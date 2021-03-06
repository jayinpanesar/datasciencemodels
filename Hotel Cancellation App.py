Python 3.10.1 (v3.10.1:2cd268a3a9, Dec  6 2021, 14:28:59) [Clang 13.0.0 (clang-1300.0.29.3)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
# Program to predict Hotel Bookings
import queue
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, IntVar, Radiobutton, Toplevel
from tkcalendar import Calendar
from functools import partial
import pandas as pd
# Import matplotlib for plotting the trees
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
hotel_type = "" # WARNING this is a global variable and essential to the workings of the models. Do not edit.

class DecisionTreeModel:

    # *****************************************************************************************************
    # This class has all the models needed to perform the predictions. If a new model is added then it should
    # be added in this class as a method. All features of the data have been included for this purpose
    #to ensure that if a new model is needed that the data includes all possible elements
    # if the model is first investigated on Kaggle then the decision tree should be plotted to make sure
    # that the trees match. The code is included in the methods here but commented out. Note the hotel_type
    #i is held in a global variable and this must not be changed to hold anything other than the type
    # The models are selected in order of priority: if the data shows a non refundable deposit type then
    # this model will be called independently of whether the hotel is a city hotel or a resort hotel. If the
    # deposit type is not non-refundable then the hotel type must be used to call the models based on lead time
    # these are methods in this class cityLeadTime and resortLeadTime
    # ******************************************************************************************************
    hotel_data = ""

    def __init__(self):
        # read in data
        self.hotel_data = pd.read_csv('bookings.csv')
        # create the cancelled column
        self.hotel_data['cancelled'] = self.hotel_data['is_canceled'].replace({1: 'Yes', 0: 'No'})

    def non_refundable_model(self, _userValues):
        # *******************************************************************************************************
        # This is the method which creates the model based on the deposit_type being non-refundable
        #*******************************************************************************************************

        #get the records in the data which have the deposit type of "Non Refund"
        nonrefundable_data = self.hotel_data[self.hotel_data['deposit_type'] == 'Non Refund'].copy()
        # define target
        y = nonrefundable_data['cancelled']
        # create an array of all the input features and define the X
        all_features = ['lead_time', 'previous_cancellations', 'previous_bookings_not_canceled', 'days_in_waiting_list',
                        'booking_changes', 'total_of_special_requests']
        X_all = nonrefundable_data[all_features]
        # perform the training-testing split
        X_all_train, X_all_test, y_all_train, y_all_test = train_test_split(X_all, y, train_size=0.8, random_state=1)
        # Define the input features
        input_features = ['previous_bookings_not_canceled']
        # create the model
        tree_model_nr = DecisionTreeClassifier(max_depth=1)
        X_all_train= X_all_train[input_features].values
        #tree_model_nr.fit(X_all_train[input_features], y_all_train)
        tree_model_nr.fit(X_all_train, y_all_train)
        #display the model (remove after testing)
        #fig, ax = plt.subplots(figsize=(18, 8))
        #plot_tree(tree_model_nr, filled=True, impurity=False, feature_names=input_features, proportion=True,
                 # class_names=["No", "Yes"], ax=ax, fontsize=10);
         #Create a list of the predictions for the test data
        #y_pred_nr = tree_model_nr.predict(X_all_test[input_features])
        X_sample_data = [[_userValues["Previous Bookings Not Cancelled"]]]
        y_predsample = tree_model_nr.predict(X_sample_data)
        return y_predsample

    def cityLeadTime(self, _userValues):
        # *******************************************************************************************************
        # This is the method which creates the model based on the lead time for the city hotel
        # The city hotel is determined by the global variable hotel_type and is determined through the first
        # screen where this decision is made by the user
        # *******************************************************************************************************

        # get the records for the city hotel out of the hotel data
        hotel_data_city = self.hotel_data[self.hotel_data['hotel'] == 'City Hotel'].copy()
        # define the target cancelled
        y = hotel_data_city['cancelled']

        # create an array of all the in features for the hotel and define the X
        all_features = ['lead_time', 'previous_cancellations', 'previous_bookings_not_canceled', 'days_in_waiting_list',
                        'booking_changes', 'total_of_special_requests']
        X_all = hotel_data_city[all_features]

        # perform the training-testing split
        X_all_train, X_all_test, y_all_train, y_all_test = train_test_split(X_all, y, train_size=0.8, random_state=1)
       # Define the input features
        input_featuresb = ['lead_time', 'days_in_waiting_list']
        text = X_all_train[input_featuresb]
        # create the model
        tree_model_lt_diwl = DecisionTreeClassifier(max_depth=3)
        tree_model_lt_diwl.fit(X_all_train[input_featuresb], y_all_train)

        # display the model
        fig, ax = plt.subplots(figsize=(18, 18))
        plot_tree(tree_model_lt_diwl, filled=True, impurity=False, feature_names=input_featuresb, proportion=True,
                  class_names=["No", "Yes"], ax=ax, fontsize=10)
       # X_sample_data = [[_userValues["Previous Bookings Not Cancelled"]]]
        X_sample_data = [[int(_userValues["Lead Time"]),int(_userValues["Number of Days in Waiting List"])]]
        y_predsample = tree_model_lt_diwl.predict(X_sample_data)
        return y_predsample

    def resortLeadTime(self, _userValues):
        # *******************************************************************************************************
        # This is the method which creates the model based on the lead time for the resort hotel
        # The resort hotel is determined by the global variable hotel_type and is determined through the first
        # screen where this decision is made by the user
        # *******************************************************************************************************
        #get the records for the resort hotel out of the hotel data
        hotel_data_resort = self.hotel_data[self.hotel_data['hotel'] == 'Resort Hotel'].copy()
        # define target cancelled
        y = hotel_data_resort['cancelled']

        # create an array of all the input features and define the X
        all_features = ['lead_time', 'previous_cancellations', 'previous_bookings_not_canceled', 'days_in_waiting_list',
                        'booking_changes', 'total_of_special_requests']
        X_all = hotel_data_resort[all_features]

        # perform the training-testing split
        X_all_train, X_all_test, y_all_train, y_all_test = train_test_split(X_all, y, train_size=0.8, random_state=1)
        # Define the input features
        input_features2 = ['lead_time', 'previous_cancellations']

        # create the model
        tree_model_lt_pc = DecisionTreeClassifier(max_depth=3)
        tree_model_lt_pc.fit(X_all_train[input_features2], y_all_train)

        # display the model
        fig, ax = plt.subplots(figsize=(18, 18))
        plot_tree(tree_model_lt_pc, filled=True, impurity=False, feature_names=input_features2, proportion=True,
                  class_names=["No", "Yes"], ax=ax, fontsize=10);
        X_sample_data = [[int(_userValues["Lead Time"]), int(_userValues["Previous Cancellations"])]]
        y_predsample = tree_model_lt_pc.predict(X_sample_data)
        return y_predsample

class ConfirmWindow(Toplevel):
    #*************************************************************************************************************
    # This window is used to confirm to the user the data that has been entered. If any changes are made
    # to the data entry fields in the main root window (Hotel App) then this class will need to be edited
    # to display this in a label/label pair. Note this should also be edited in the userValues dictionary
    #*************************************************************************************************************
    result = ""
    def __init__(self, _root_window, _userValues):
        start_row = 1
        super().__init__()
        self.geometry("500x500")
        self.title("Confirm")
        self.configure(bg="green")  # set the background colour
        btn_confirm = Button(self, text="Get Results", command=lambda: self.get_results(_userValues))
        btn_confirm.configure(width=20, height=5)
        btn_confirm.grid(row=18, column=1)
        btn_back = Button(self, text="Back", command=lambda: self.establish_Main_Window(_root_window))
        btn_back.configure(width=20, height=5)
        btn_back.grid(row=18, column=2)
       # btn_add = Button(self, text="Add for Processing", command=lambda: self.add_to_queue(_data_queue, _userValues, _root_window))
       # btn_add.configure(width=20, height=5)
      #  btn_add.grid(row=24, column=2)
        lbl_firstname_ = Label(self, width=30, font="Arial 10", text="Firstname:", fg="white", bg="green")
        lbl_firstname_.grid(row=start_row, column=1)
        lbl_firstname = Label(self, width=30, font="Arial 10", text=_userValues["Firstname"], fg="white", bg="green")
        lbl_firstname.grid(row=start_row, column=2)
        lbl_surname_ = Label(self, width=30, font="Arial 10", text="Surname:", fg="white", bg="green")
        lbl_surname_.grid(row=start_row + 1, column=1)
        lbl_surname = Label(self, width=30, font="Arial 10", text=_userValues["Surname"], fg="white", bg="green")
        lbl_surname.grid(row=start_row + 1, column=2)
        lbl_cancellations_ = Label(self, width=30, font="Arial 10", text="Previous Cancellations",
                                   fg="white", bg="green")
        lbl_cancellations_.grid(row=start_row + 2, column=1)
        lbl_cancellations = Label(self, width=30, font="Arial 10", text=_userValues["Previous Cancellations"],
                                  fg="white", bg="green")
        lbl_cancellations.grid(row=start_row + 2, column=2)
        lbl_prev_cancellations_ = Label(self, width=30, font="Arial 10",
                                        text="Previous Bookings Not Cancelled",
                                        fg="white", bg="green")
        lbl_prev_cancellations_.grid(row=start_row + 3, column=1)
        lbl_prev_cancellations = Label(self, width=30, font="Arial 10",
                                       text=_userValues["Previous Bookings Not Cancelled"],
                                       fg="white", bg="green")
        lbl_prev_cancellations.grid(row=start_row + 3, column=2)
        lbl_special_requests_ = Label(self, width=30, font="Arial 10", text="Number of Special Requests", fg="white",
                                      bg="green")
        lbl_special_requests_.grid(row=start_row + 4, column=1)
        lbl_special_requests = Label(self, width=30, font="Arial 10", text=_userValues["Number of Special Requests"],
                                     fg="white", bg="green")
        lbl_special_requests.grid(row=start_row + 4, column=2)
        lbl_days_waiting_ = Label(self, width=30, font="Arial 10", text="Number of Days in Waiting List",
                                  fg="white", bg="green")
        lbl_days_waiting_.grid(row=start_row + 5, column=1)
        lbl_days_waiting = Label(self, width=30, font="Arial 10", text=_userValues["Number of Days in Waiting List"],
                                 fg="white", bg="green")
        lbl_days_waiting.grid(row=start_row + 5, column=2)
        lbl_deposit_type_ = Label(self, width=30, font="Arial 10", text="Deposit Type",
                                  fg="white", bg="green")
        lbl_deposit_type_.grid(row=start_row + 6, column=1)
        lbl_deposit_type = Label(self, width=30, font="Arial 10", text=_userValues["Deposit Type"],
                                 fg="white", bg="green")
        lbl_deposit_type.grid(row=start_row + 6, column=2)
        lbl_market_segment_type_ = Label(self, width=30, font="Arial 10", text="Market Segment",
                                         fg="white", bg="green")
        lbl_market_segment_type_.grid(row=start_row + 7, column=1)
        lbl_market_segment_type = Label(self, width=30, font="Arial 10", text=_userValues["Market Segment"],
                                        fg="white", bg="green")
        lbl_market_segment_type.grid(row=start_row + 7, column=2)
        lbl_booking_date_ = Label(self, width=30, font="Arial 10", text="Booking Date",
                                   fg="white", bg="green")
        lbl_booking_date_.grid(row=start_row + 8, column=1)
        lbl_booking_date_ = Label(self, width=30, font="Arial 10", text=_userValues["Booking Date"],
                                  fg="white", bg="green")
        lbl_booking_date_.grid(row=start_row + 8, column=2)
        lbl_check_in_date_ = Label(self, width=30, font="Arial 10", text="Check in Date",
                                    fg="white", bg="green")
        lbl_check_in_date_.grid(row=start_row + 9, column=1)
        lbl_check_in_date = Label(self, width=30, font="Arial 10", text=_userValues["Check in Date"],
                                   fg="white", bg="green")
        lbl_check_in_date.grid(row=start_row + 9, column=2)
        lbl_leadtime_ = Label(self, width=30, font="Arial 10", text="Lead Time",
                                   fg="white", bg="green")
        lbl_leadtime_.grid(row=start_row + 11, column=1)
        lbl_leadtime = Label(self, width=30, font="Arial 10", text=_userValues["Lead Time"],
                                  fg="white", bg="green")
        lbl_leadtime.grid(row=start_row + 11, column=2)
        lbl_result_ = Label(self, width=30, font="Arial 10", text="Result", fg="white", bg="green")
        lbl_result_.grid(row=24, column=1)

   # def add_to_queue(self, thisdataqueue, _userValues, _root_window):

    #************************************************************************************************************
    # The adding to the queue works but the development work to remove and process the queue has not been completed
    # This could be done here
    #**************************************************************************************************************

       # thisdataqueue.enqueue(_userValues)
       # self.establish_Main_Window(_root_window)

    def establish_Main_Window(self, _root_window):
        # establish the main window and close the confirmation window
        self.destroy()
        _root_window.update()
        _root_window.deiconify()

    def get_results(self, _userValues):
        global hotel_type
        resultmodel = DecisionTreeModel()
        # build array with data
        if _userValues["Deposit Type"] == "You have selected the option Non-Refundable Deposit":
            # check non-refundable first as if this is selected it will override the other lead time model
            self.result = resultmodel.non_refundable_model(_userValues)
        elif hotel_type == "Resort":
            #call the lead time model for the resort hotel
            self.result = resultmodel.resortLeadTime(_userValues)
        else:
            #call the lead time model for the city hotel
            self.result = resultmodel.cityLeadTime(_userValues)
        lbl_result = Label(self, width=30, font="Arial 10", text=self.result[0,], fg="white", bg="green")
        lbl_result.grid(row=26, column=1)

#class dataQueue:
 #   thisdataqueue = queue.Queue()
#
 #   def __init__(self):
 #       pass

 #   def enqueue(self, _UserValues):
#        _queueNode =  queueNode(_UserValues)
#        self.thisdataqueue.put(_queueNode)


#class queueNode:
#    qUserValues = tuple

#    def __init__(self, _userValues):
 #      self.qUserValues = (_userValues["Firstname"], _userValues["Surname"], _userValues["Previous Cancellations"],
 #                           _userValues["Previous Bookings Not Cancelled"], _userValues["Number of Special Requests"],
#                            _userValues["Number of Days in Waiting List"], _userValues["Market Segment"],
#                            _userValues["Deposit Type"], _userValues["Check in Date"], _userValues["Booking Date"],
 #                           _userValues["Lead Time"])



# *********************************HOTEL APP CLASS*******************************************************************

class HotelApp(Tk):
    start_row = 3  # starting row for the data entry aspects
    column_left_labels = 0  # starting column for the labels in the left hand column
    column_left_text = 1  # starting column for the text boxes in the left hand column
    column_right_labels = 4  # starting column for the labels in the right hand column
    column_right_text = 5  # starting column for the text boxes in the right hand column
    market_radio_selection = ""
    dep_radio_selection = ""

    # Dictionary to store the deposit radio button values
    Radio_Deposit_Values = {"No Deposit": 1,
                            "Refundable Deposit": 2,
                            "Non-Refundable Deposit": 3}
    # Dictionary to store the market segment radio button values
    Radio_Market_Segment_Values = {"Online TA": 1,
                                   "Offline TA": 2,
                                   "Direct": 3,
                                   "Corporate": 4,
                                   "Groups": 5}
    # Dictionary to store the user data from the form
    UserValues = {"Firstname": "",
                  "Surname": "",
                  "Previous Cancellations": 0,
                  "Previous Bookings Not Cancelled": 0,
                  "Number of Special Requests": 0,
                  "Number of Days in Waiting List": 0,
                  "Market Segment": "",
                  "Deposit Type": "",
                  "Check in Date": "",
                  "Booking Date": "",
                  "Lead Time": ""}

    def __init__(self):
        # The constructor will build the user interface and call the validation routines.

        super().__init__()  # call the constructor of the Tk class
        self.geometry("1200x800")  # size the window
        self.configure(bg="green")  # set the background colour
        title = Label(
            text="Please Enter Guest Details",
            foreground="white",  # Set the text color to white
            background="green",  # Set the background color to green
            font=("Arial", 25)
        )
        title.grid(column=1, columnspan=3)
        # Setup the label entry pairs
        # Firstname
        txt_firstname = Entry(self, width=20, font="Arial 10")
        lbl_firstname = Label(self, width=12, font="Arial 10", text="Enter Firstname", fg="white", bg="green")
        lbl_firstname.grid(row=self.start_row, column=self.column_left_labels)
        txt_firstname.grid(row=self.start_row, column=self.column_left_text)
        # Surname
        txt_surname = Entry(self, width=20, font="Arial 10")
        lbl_surname = Label(self, width=12, font="Arial 10", text="Enter Surname", fg="white", bg="green")
        lbl_surname.grid(row=self.start_row, column=self.column_right_labels)
        txt_surname.grid(row=self.start_row, column=self.column_right_text)
        # Cancellations
        txt_cancellations = Entry(self, width=20, font="Arial 10")
        lbl_cancellations = Label(self, width=18, font="Arial 10", text="Previous Cancellations", fg="white",
                                  bg="green")
        lbl_cancellations.grid(row=self.start_row + 2, column=self.column_left_labels)
        txt_cancellations.grid(row=self.start_row + 2, column=self.column_left_text)
        # Previous Bookings
        txt_prev_cancellations = Entry(self, width=20, font="Arial 10")
        lbl_prev_cancellations = Label(self, width=25, font="Arial 10", text="Previous Bookings not Cancelled",
                                       fg="white",
                                       bg="green")
        lbl_prev_cancellations.grid(row=self.start_row + 2, column=self.column_right_labels)
        txt_prev_cancellations.grid(row=self.start_row + 2, column=self.column_right_text)
        # Special Requests
        txt_special_requests = Entry(self, width=20, font="Arial 10")
        lbl_special_requests = Label(self, width=25, font="Arial 10", text="Number of Special Requests", fg="white",
                                     bg="green")
        lbl_special_requests.grid(row=self.start_row + 4, column=self.column_left_labels)
        txt_special_requests.grid(row=self.start_row + 4, column=self.column_left_text)
        # Days Wait List
        txt_days_waiting = Entry(self, width=20, font="Arial 10")
        lbl_days_waiting = Label(self, width=25, font="Arial 10", text="Number of Days in Waiting List", fg="white",
                                 bg="green")
        lbl_days_waiting.grid(row=self.start_row + 4, column=self.column_right_labels)
        txt_days_waiting.grid(row=self.start_row + 4, column=self.column_right_text)

        # ************************************************RADIO BUTTONS*****************************************************
        # define the radio buttons for the deposit type

        var = IntVar()
        lbl_deposit = Label(self, width=15, font="Arial 10", text="Deposit Type", fg="white", bg="green")
        lbl_deposit.grid(row=self.start_row + 12, column=self.column_right_labels)
        lbl_deposit_radio = Label(self, width=40, font="Arial 10", text="", fg="white", bg="green")
        lbl_deposit_radio.grid(row=self.start_row + 15, column=self.column_right_text)

        # create the radio buttons
        count = 10
        for (text, value) in self.Radio_Deposit_Values.items():
            Radiobutton(self, text=text, variable=var, value=value, bg="green", fg="white", command=lambda:
            self.sel_radio_result(lbl_deposit_radio, var, self.Radio_Deposit_Values)).grid(
                row=self.start_row + count, column=self.column_right_labels + 1, sticky="W")
            count = count + 2

        # **************************************************************************************************************
        # define the radio buttons for the market segment

        var1 = IntVar()
        lbl_market_segment = Label(self, width=15, font="Arial 10", text="Market Segment", fg="white", bg="green")
        lbl_market_segment.grid(row=self.start_row + 19, column=self.column_right_labels)
        lbl_market_segment_result = Label(self, width=30, font="Arial 10", text="", fg="white", bg="green")
        lbl_market_segment_result.grid(row=self.start_row + 25, column=self.column_right_text)

        # create the radio buttons
        count = 16
        for (text, value) in self.Radio_Market_Segment_Values.items():
            Radiobutton(self, text=text, variable=var1, value=value, bg="green", fg="white", command=lambda:
            self.sel_radio_result(lbl_market_segment_result, var1, self.Radio_Market_Segment_Values)).grid(
                row=self.start_row + count, column=self.column_right_labels + 1, sticky="W")
            count = count + 2

        # ****************************************** CALENDAR OBJECTS **************************************************

        # create the calendar checkin object
        calbooking = Calendar(self, selectmode='day',
                              year=2022, month=5,
                              day=22)

        # display the calendar
        calbooking.grid(row=self.start_row + 15, column=self.column_left_text)

        # create the calendar checkout object
        calcheckin = Calendar(self, selectmode='day',
                               year=2022, month=5,
                               day=22)

        # display the calendar
        calcheckin.grid(row=self.start_row + 25, column=self.column_left_text)

        date = Label(self, width=20, text="", fg="white", bg="green")

        checkindate = Label(self, width=20, text="", fg="white", bg="green")

        # Add Button and Label for the dates
        Button(self, text="Select the date of booking",
               command=partial(self.booking_date, date, calbooking, calcheckin)).grid(
            row=self.start_row + 16,
            column=self.column_left_text)
        Button(self, text="Select check in date", command=partial(self.checkin_date, calbooking, calcheckin,
                                                                   checkindate)).grid(
            row=self.start_row + 26,
            column=self.column_left_text)

        date.grid(row=self.start_row + 18, column=self.column_left_text)
        checkindate.grid(row=self.start_row + 30, column=self.column_left_text)

        # ***************** SUBMIT BUTTON ***********************************************************************
        Button(self, text="Confirm", width=20, height=5, command=
        lambda: self.collect_data(txt_firstname, txt_surname, txt_cancellations, txt_prev_cancellations,
                                  txt_special_requests, txt_days_waiting, calcheckin, calbooking,
                                  lbl_firstname, lbl_surname, lbl_cancellations, lbl_prev_cancellations,
                                  lbl_days_waiting, lbl_special_requests, lbl_deposit_radio, lbl_deposit,
                                  lbl_market_segment_result, lbl_market_segment)).grid \
            (row=self.start_row + 26, column=self.column_right_text)

        # ******************************* OPEN THE SPLASH SCREEN ************************************************
        self.withdraw()
        splashWindow = splashScreen(self)
        self.wait_window(splashWindow)

        # ********************************** END OF CONSTRUCTOR **************************************************
    def booking_date(self, _date, _calbooking, calendar_checkin):
        if calendar_checkin.get_date() < _calbooking.get_date():
            _date.config(text="Invalid date selected", bg="red")
        else:
            _date.config(text="Booking date is: " + _calbooking.get_date(), fg="white", bg="green")

    def checkin_date(self, calendar_booking, calendar_checkin, _checkindate):
        # This validates that the check in date is after the booking date and then displays a date invalid message
        # or the date of check in.

        if calendar_booking.get_date() > calendar_checkin.get_date():
            _checkindate.config(text="Invalid date selected", bg="red")
        else:
            _checkindate.config(text="Check in date is: " + calendar_checkin.get_date(), fg="white", bg="green")

    def sel_radio_result(self, _lbl_market, _var, _dictvalue):
        value = _var.get()
        key = [k for k, v in _dictvalue.items() if v == value]

        selection = "You have selected the option " + str(key[0])
        if _dictvalue == self.Radio_Deposit_Values:
            self.dep_radio_selection = selection
        else:
            self.market_radio_selection = selection

        _lbl_market.config(text=selection)

    def get_radio_result(self, _var, _dictvalue):
        value = _var.get()
        key = [k for k, v in _dictvalue.items() if v == value]
        return str(key[0])


    def calculate_lead_time(self, _dateBooking, _checkindate):
        leadTime = (_dateBooking - _checkindate)
        days_ = leadTime.days
        if days_ < 0:
            days_ = days_ * -1
        return days_

    # *********************************************COLLECT DATA***********************************************************
    def collect_data(self, _txt_firstname, _txt_surname, _txt_cancellations, _txt_previous_not_cancelled,
                     _txt_special_requests, _txt_days_waiting, _calCheckin, _calBooking, _lbl_firstname,
                     _lbl_surname, _lbl_cancellations, _lbl_prev_cancellations, _lbl_days_waiting,
                     _lbl_special_requests,
                     _lbl_deposits, _lbl_dep_, _lbl_market_result, _lbl_market):
        booking_date = _calBooking.selection_get()
        checkin_date = _calCheckin.selection_get()

        leadTime= self.calculate_lead_time(booking_date, checkin_date)

        valid = True
        # Validation of the data entry fields
        if not _txt_firstname.get():
            _lbl_firstname.configure(bg="red")
            valid = False
        else:
            _lbl_firstname.configure(bg="green")
        if not _txt_surname.get():
            _lbl_surname.configure(bg="red")
            valid = False
        else:
            _lbl_surname.configure(bg="green")
        if not _txt_cancellations.get():
            _lbl_cancellations.configure(bg="red")
            valid = False
        else:
            _lbl_cancellations.configure(bg="green")
        if not _txt_previous_not_cancelled.get():
            _lbl_prev_cancellations.configure(bg="red")
            valid = False
        else:
            _lbl_prev_cancellations.configure(bg="green")
        if not _txt_days_waiting.get():
            _lbl_days_waiting.configure(bg="red")
            valid = False
        else:
            _lbl_days_waiting.configure(bg="green")
        if not _txt_special_requests.get():
            _lbl_special_requests.configure(bg="red")
            valid = False
        else:
            _lbl_special_requests.configure(bg="green")
        if not _lbl_deposits.cget("text"):
            _lbl_dep_.configure(bg="red")
            valid = False
        else:
            _lbl_dep_.configure(bg="green")
        if not _lbl_market_result.cget("text"):
            _lbl_market.configure(bg="red")
            valid = False
        else:
            _lbl_market.configure(bg="green")

        # this statement will gather the data into a dictionary for submission to the prediction model
        # add the values to the dictionary

        if valid:
            self.UserValues["Firstname"] = _txt_firstname.get()
            self.UserValues["Surname"] = _txt_surname.get()
            self.UserValues["Previous Cancellations"] = _txt_cancellations.get()
            self.UserValues["Previous Bookings Not Cancelled"] = _txt_previous_not_cancelled.get()
            self.UserValues["Number of Special Requests"] = _txt_special_requests.get()
            self.UserValues["Number of Days in Waiting List"] = _txt_days_waiting.get()
            self.UserValues["Market Segment"] = self.market_radio_selection
            self.UserValues["Deposit Type"] = self.dep_radio_selection
            self.UserValues["Booking Date"] = booking_date
            self.UserValues["Check in Date"] = checkin_date
            self.UserValues["Lead Time"] = leadTime
            # open the confirm window which will display the data
            self.open_confirm_window()

    def open_confirm_window(self):
        self.withdraw()
        window = ConfirmWindow(self, self.UserValues)
        window.grab_set()

    def show(self):
        # self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()


# ***********************************************end of hotel app class***************************************************
class HotelCancellationModel:

    def __init__(self):
        pass

    def get_outcome(self, _userValues):
        if _userValues["Deposit Type"] == "You have selected the option Refundable Deposit" and \
                _userValues["Previous Cancellations"]:
            return True

#******************************************Splash Screen Class*********************************************************
class splashScreen(Toplevel):

    def __init__(self, _rootWindow):
        super().__init__()
        self.geometry("410x200")
        self.configure(bg="green")  # set the background colour
        self.title("Hotel Application")
        lbl_title = Label(self,text="Please Select the Hotel related to the Enquiry",foreground="white",  # Set the text color to white
            background="green",  # Set the background color to green
            font=("Arial", 15))
        lbl_title.grid(row = 1, column=1, columnspan=2)
        #place the resort button in the Window
        btn_resort = Button(self, text="Resort", command=lambda: self.set_hotelTypeResort(_rootWindow))
        btn_resort.configure(width=20, height=5)
        btn_resort.grid(row=2, column=1)
        # place the city button in the Window
        btn_city = Button(self, text="City", command=lambda: self.set_hotelTypeCity(_rootWindow))
        btn_city.configure(width=20, height=5)
        btn_city.grid(row=2, column=2)

    def set_hotelTypeResort(self,_rootWindow):
        # this procedure will set the hotel_type to resort and then destroy the opening window and re-establish the main window
        global hotel_type
        hotel_type = "Resort"
        self.destroy()
        self.establish_Main_Window(_rootWindow)
    def set_hotelTypeCity(self, _rootWindow):
        # this procedure will set the hotel_type to city and then destroy the opening window and re-establish the main window
        global hotel_type
        hotel_type = "City"
        self.destroy()
        self.establish_Main_Window(_rootWindow)
    def establish_Main_Window(self, _root_window):
        # establish the main window and close the confirmation window
        _root_window.update()
        _root_window.deiconify()



#********************************************* end of splash screen class *******************************************

# Start of Main Program
# establish the queue for the processing of the elements but with a size of 0

if __name__ == '__main__':
#    data_queue = dataQueue()
    hotel_app = HotelApp()
    hotel_app.mainloop()  # starts the main event handler