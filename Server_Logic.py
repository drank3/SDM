from PySide2 import QtSql
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
from PySide2.QtCore import Qt
import time

ui = [None]
bl = [None]

class Server_Logic():

    def __init__(self, uix, blx):
        global ui, bl
        ui = uix
        bl = blx
        self.connection_status = False
        self.Create_Server_Connection()



    def Sync(self):
        dialog_box = ui.Show_Dialog("Server Connection to EML", "Database modification rights still limited with general users, please proceed with caution")
        dialog_box.exec()
        devices_data, checked_items = bl.Return_Checked_Info()

        if str(type(devices_data))==r"<class 'pandas.core.frame.DataFrame'>":
            try:
                for index, device in devices_data.iterrows():
                    self.Insert_New_Device(device['Name'], device['Batch'], device['Data'])
                    device_item = [item for item in checked_items if item.text(0)==device['Name']][0]
                    ui.BUI.Change_Item_Color(device_item, "green")
                    device_item.setCheckState(0, Qt.CheckState.Unchecked)

            except Exception as e:
                print(f"Database sync (final) failed with code: {e}")





    def Create_Server_Connection(self):
        start_time = time.perf_counter()

        connection = None

        #This part will attempt to establish a connection until 10 s is reached,
        # at which point it will give up, and raise an error
        time_elapsed = time.perf_counter()-start_time
        timeout_time = 5    #The amount of seconds required for a timeout

        while time_elapsed < timeout_time:
            try:
                connection = mysql.connector.connect(
                    host='170.187.158.29',
                    user='remote_user',
                    passwd='eml-lab293461',
                    database = 'EML'
                )
                self.connection_status = True
                self.connection = connection
                print("MySQL Database connection successful")
                return self.connection_status

            except Exception as e:
                print(f"Server error: {e}")
                self.connection_status = False

            time_elapsed = time.perf_counter()-start_time

        if time_elapsed >= timeout_time:
            print("Server connection timed out")





        self.connection = connection




    def Insert_New_Device(self, device_name, batch_name, data):
        if self.connection_status == True:
            try:
                cursor = self.connection.cursor()
                query_read = "SELECT Device_ID FROM List_of_Devices ORDER BY Device_ID DESC LIMIT 1"
                cursor.execute(query_read)

                try:
                    last_value = int(cursor.fetchall()[0][0])
                except Exception as e:
                    last_value = 0

                device_id = last_value+1

                user = ui.user

                #SQL doesn't like apostrophes in data, so  need to double them up wherever they are
                user = user.replace(r"'", r"''")
                data = str(data).replace(r"'", r"''")
                device_name = device_name.replace(r"'", r"''")
                batch_name = batch_name.replace(r"'", r"''")

                query_add = f"INSERT INTO List_of_Devices(Device_ID, Device_Name, Batch_Name, Date_Added, Group_Member, Data) VALUES({device_id}, \'{device_name}\', \'{batch_name}\', \'{current_date}\', \'{user}\', \'{data}\');"
                current_date = str(datetime.now())

                cursor.execute(query_add)
                self.connection.commit()
                cursor.close()
                return True

            except Exception as e:
                print(f"Database sync failed with error: {e}")
                return False
            else:
                print("No connection was established. Try setting that up and trying again")

if __name__ == "__main__":
    sl = Server_Logic("ssssdfsdfsdfdsf", "sdfsdfad")
    sl.Create_Server_Connection()
    sl.Insert_New_Device("Paul", "chrrsss", "hehehe")
