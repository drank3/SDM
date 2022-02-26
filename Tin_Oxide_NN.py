import torch
from torch import nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import os
import csv
from sklearn.preprocessing import OneHotEncoder
import math
import random
from random import randrange
import itertools



class Data_Processor():
    def __init__(self):
        #This is the raw output matrix representing a set of devices parameters and characterization
        self.all_data = []

        #All the data we care about for ML regression
        self.target_data = pd.DataFrame()

        #The parameter that is optimized with the ml algorithm
        self.par_to_optimize = 'PCE[%] Rv'

        #The names of all of the electrical parameters
        self.electrical_parameter_names = ['PCE[%] Rv', 'PCE[%] Fw', 'Voc[V] Rv', 'Voc[V] Fw', 'FF[%] Rv',
                                      'FF[%] Fw', 'Jsc[mA/cm2] Rv', 'Jsc[mA/cm2] Fw', 'Stabilized_MPP [%]']


    def Import_From_CSV(self, path):

        with open(path) as file:
            reader = csv.reader(file, delimiter = ',')
            names = ''
            for row in reader:
                if row[0]=="Variable":
                    names = row
                elif row[0] == "Value":
                    self.all_data.append(pd.DataFrame(row, index=names))

        self.Group_Data()

    #Organizes the data into groups based on the devices' architectures (material stacks)
    #Creates a dict with one entry per group with the key names as the group architecture
    #self.all_data must be filled before using this function
    def Group_Data(self):
        #Each member in a group must have the exact same parameters (same path for all layers)
        grouped_list = []
        for pixel in self.all_data:
            matched = False
            for group in grouped_list:
                if list(pixel.index) == list(group[0].index):

                    matched=True
                    group.append(pixel)
            if not matched:
                grouped_list.append([pixel])


        group_names = []
        #Creating names for each of the groups of data, created based on material type
        for group in grouped_list:
            layer_count = 1
            item=group[0]
            name=''
            break_cond=False
            while not break_cond:
                name+=item.loc[f'Layer {layer_count}_Material', 0]
                try:
                    item.loc[f'Layer {layer_count+1}_Material', 0]
                    layer_count+=1
                    name+='-'
                except Exception as e:
                    break_cond = True
            #Adds a number to the end of the group name if it's a duplicate
            if any([prev_name.__contains__(name) for prev_name in group_names]):
                name = name + '_'+str(sum([prev_name.__contains__(name) for prev_name in group_names]))

            group_names.append(name)

        self.grouped_data = {}
        for i in range(0, len(grouped_list), 1):
            name = group_names[i]
            data = grouped_list[i]

            self.grouped_data[name] = data

    #This function fills in self.target_data with all the pixels from
    def Select_Target(self, names_list):
        if len(names_list) == 1:

            target_group = self.grouped_data[names_list[0]]

            target_df = pd.DataFrame()

            for pixel_data in target_group:
                device = pixel_data.loc['Device', 0]
                pixel_name = pixel_data.loc['Pixel', 0]
                #Csv's are broken, saving imaginary "Structure" pixels. Some bug somewhere in the source. Will fix one day
                if pixel_name=="Structure":
                    pass
                else:
                    name = device + ' - ' + pixel_name
                    target_df[name] = pixel_data[0]

        else:
            #TODO: Fill in this case for when we want to look at multiple groups simulatenously
            pass

        self.target_data = target_df

    #Main role is to remove parameters who's values do not change for any device
    #Also Removes unnesecary variables from self.target_data and fills np.Nan with 0 (artifact from Carlo's importer)
    def Clean_Data(self):
        #Cleaning up the garbage variables

        self.target_data.drop('Variable', inplace=True)
        self.target_data.drop("Batch", inplace = True)
        self.target_data.drop("Pixel", inplace = True)
        #I pick up a bunch of empty columns somewhere, so I drop them here
        self.target_data = self.target_data.replace('', np.NaN).dropna(how='all')


        #Removing rows who's values do not change in all devices
        for index in self.target_data.index.values:
            values  = self.target_data.loc[index].values

            if (values[0]==values).all():
                if index:
                    self.target_data = self.target_data.drop(index)

            #Removing unitsand converting to float
            #TODO: Make something more elegant than this, info in units is being discarded
            else:
                new_values = []
                for value in values:
                    if isinstance(value, str) and (index != 'Device'):
                        value = value.split(' ')[0]
                        try:
                            value = float(value)
                        except:
                            pass
                    new_values.append(value)
                self.target_data.loc[index] = new_values

        self.target_data = self.target_data.fillna(0)
        self.target_data = self.target_data.transpose()
        self.target_data = self.target_data.sample(frac=1)

    #Drops all "bad" pixels from a device with a method decided by a string input mode. if mode is "Average", avery pixel in a device below its average is dropped
    # if mode is "Max" then every pixel below the device's champion pixel is dropped (leaves one pixel per device)
    def Drop_Bad_Pixels(self, mode):

        devices_list = list(dict.fromkeys(list(self.target_data['Device'].values)))

        for device in devices_list:
            pixels = self.target_data.loc[self.target_data['Device'] == device]
            av_opt = pixels[self.par_to_optimize].mean()
            max_opt = pixels[self.par_to_optimize].max()

            if mode == "Average":
                #Everything below the device average is dropped
                bad_pixels = pixels[pixels[self.par_to_optimize] <= 1.0*av_opt ]
            elif mode == "Max":
                #I'm dropping everything that's not the best pixel here
                bad_pixels = pixels[pixels[self.par_to_optimize] < max_opt ]
                #Directly Dropping pixels with the duplicate values from the same device
                if len((pixels[pixels[self.par_to_optimize] == max_opt]).index) > 1:
                    repeat_indexes = (pixels[pixels[self.par_to_optimize] == max_opt]).index[1:]

            self.target_data.drop(bad_pixels.index, inplace=True)

    #Generates the training and testing sets for ml regression, with train ratio as a 0-1 value for the training set to testing set size ratio
    #Also randomizes and organizes the data
    def Generate_Sets(self, train_ratio):
        #Creating training and testing sets
        data_sep = int(train_ratio* len(self.target_data.index.values)  -1)
        train_df = self.target_data.iloc[range(0, data_sep, 1)]
        test_df = self.target_data.iloc[range(data_sep, len(self.target_data.index.values)-1, 1)]


        train_output = train_df[self.par_to_optimize]
        train_input = train_df.drop(self.electrical_parameter_names, axis=1)

        test_output = test_df[self.par_to_optimize]
        test_input = test_df.drop(self.electrical_parameter_names, axis=1)

        return train_input, test_input, train_output, test_output


    #Makes sure that floats are floats, and converts string (categorical) values into encoded numbers
    #Also calls to Sort_By_Devices, which finishes out data sorting and removes the Device column
    def Parameter_Encoder(self):

        for column in self.target_data.columns.values:
            encoder = OneHotEncoder()
            try:
                #Converting every float column to float data type to be sure
                self.target_data[column] = self.target_data[column].astype(np.float)
            except Exception as e:
                #Encoding every column that can't be converted to float

                #Fitting the OneHotEncoder to the categorical column
                encoder.fit(self.target_data[[column]])
                categories = encoder.categories_[0]

                #Generating the encoded array output for the column
                encoded_column = encoder.transform(self.target_data[[column]]).toarray()
                self.target_data.drop(column, axis=1, inplace=True)

                #Adding the encoded results of the inital column to the
                categories_names = [str(column+'='+category) for category in categories]
                print(categories)
                print(categories_names)
                encoded_df = pd.DataFrame(encoded_column, columns = categories_names, index=self.target_data.index)
                self.target_data = pd.concat([self.target_data, encoded_df], axis=1)



    #Sorts the data randomly by device (pixels from the same device are grouped together) and removes the Device variable from self.target_data
    def Sort_By_Device(self):
        devices = list(set(list(self.target_data['Device'].values)))
        rand_list = [random.randint(0, 10000) for i in range(len(devices))]
        rand_as = pd.DataFrame(rand_list, index = devices)

        for device in devices:
            self.target_data.loc[self.target_data['Device']==device, 'Device'] = rand_as.loc[device].values[0]


        self.target_data.sort_values(by=['Device'], inplace=True)
        self.target_data.drop('Device', axis=1, inplace=True)



if __name__ == "__main__":

    #This is all you need to generate the testing and training sets
    #-------------------------------------------------------------------------------------------------
    dp = Data_Processor()
    dp.Import_From_CSV('Tin_Oxide_Optimization.csv')
    print(f"Group Names: {list(dp.grouped_data.keys())}")
    dp.Select_Target(['Glass-FTO-Sn02-Perovskite-Spiro-OMeTAD-Gold'])
    dp.Clean_Data()
    #Max or Average, see function description
    dp.Drop_Bad_Pixels("Max")
    dp.Sort_By_Device()
    dp.Parameter_Encoder()
    train_input, test_input, train_output, test_output = dp.Generate_Sets(.8)
    tensor_input = torch.Tensor(train_input.values)
    tensor_output = torch.Tensor(train_output.values)
    print(train_input)
    print(tensor_input)
    print(train_output)
    print(tensor_output)
    #-------------------------------------------------------------------------------------------------

# model = torch.nn.Sequential(
#     torch.nn.Linear(5, 1),
#     torch.nn.Flatten(0, 1)
# )
#
# loss_fn = torch.nn.MSELoss(reduction='sum')
# x = torch.nn.Parameter(tensor_input, requires_grad = True)
# y = tensor_output
# #how fast values converge during gradient descent
# learning_rate = 1e-3
#
# optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)
# for t in range(19):
#     y_predicted = model(x)
#
#     loss = loss_fn(y_predicted, y)
#     if t % 100 == 99:
#         print(t, loss.item())
#
#     optimizer.zero_grad()
#
#     loss.backward()
#
#     optimizer.step()
#
# linear_layer = model[0]
# print(f'Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} par 1 + {linear_layer.weight[:, 1].item()} par2 + {linear_layer.weight[:, 2].item()} par3 + {linear_layer.weight[:, 2].item()} par4 + {linear_layer.weight[:, 2].item()} par5')

#following gradient nn tutorial

    x = tensor_input
    y = tensor_output

    n_samples, n_features = x.shape
    print (x.shape)
    input_size = n_features
    output_size = 1

    #model prediction
    class LinearRegression(nn.Module):
        def __init__(self, input_dim, output_dim):
            super(LinearRegression, self).__init__()
            self.fc1 = nn.Linear(input_dim, output_dim)
            print(self.fc1)

        def forward(self, x):
            # x = torch.flatten(x, 1)
            # x = F.relu(self.fc1(x))
            x = self.fc1(x)
            return x

    model = LinearRegression(input_size, output_size)
    #training
    learning_rate = 1e-3
    n_iters = 10

    #calc loss
    loss = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)
    for epoch in range(n_iters):
        #prediction = forward pass
        y_pred = model(x)
        #loss
        l = loss(y_pred, y)

        #gradients
        l.backward()

        #update weights
        optimizer.step()
        #zero gradients
        optimizer.zero_grad()

        if epoch %1 == 0:
            [w, b] = model.parameters()
            print(f'epoch {epoch + 1}: w = {w[0][0].item():.3f}, loss = {l:.8f}')
    print(f'Prediciton after training: f(5) = {model(x):.3f}')
