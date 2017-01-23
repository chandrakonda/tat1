'''
Test cases for Apptio
'''
# TODO : Need to check pytest.ini file
# TODO : Need to compare framework with Udemy framework and make improvements

# TODO # Need to create XL report
# Sathish
# TODO # Includes and excluded - need to check for headers - Complete - 22/1/2017
# TODO # Update data - come with plan
# 01/05/2017
# TODO # Select and unselect
# 1/22/2017
# TODO # No run test cases are marked as PASSED. Need to check that


import pytest, time , logging
from apptio_automation.Apptio.Json_Helpers.JsonHelpers import JsonHelpers
from apptio_automation.Apptio.Pages.Login_page import LoginPage
from apptio_automation.Apptio.Pages.TBMCouncil_page import TbmCouncilPage as tbmpage
from apptio_automation.Framework.Environment_setup import ConfigValuesToDictionary
import apptio_automation.Framework.Extensions.Custom_logger as  cl

from apptio_automation.Apptio.Common import Apptio_Common
from apptio_automation.Apptio.Common.Constants import Constant_Values
#--html=c:\workingdirectory\att\sample3.html --verbose --tb=short
@pytest.mark.usefixtures("apptio_setup","function_setup","jsonfileversion")
class Test_Functional():

    log = cl.customLogger(logging.DEBUG)
    col1_id_value, col1_label_value = None,None

###################################################################################################################################
# Validate first column values in the application
###################################################################################################################################

    def test_1_login_into_application(self,jsonfileversion):
        try:
            time.sleep(3)
            #pdb.set_trace()
            print (jsonfileversion)
            obj_login_page =  LoginPage()
            user_name = ConfigValuesToDictionary.get_key_value('loginuser')
            pass_word =  ConfigValuesToDictionary.get_key_value("loginpassword")
            if obj_login_page.login(user_name,pass_word,jsonfileversion):
                time.sleep(3)
            else:
                pytest.fail("Test case failed")
        except Exception as e:
            self.log.exception("Exception . Test case failed")
            pytest.fail(e)

###################################################################################################################################
# Validate first column values in the application
###################################################################################################################################
    def test_2_validate_first_column_category_values_with_given_json(self,json_data):
        try:
        #pdb.set_trace()
            __local_tbm_page_obj = tbmpage()
            Test_Functional.col1_id_value, Test_Functional.col1_label_value = __local_tbm_page_obj.check_and_get_category_values(0)  # get first col values from application
            # get first child values from JSON
            __local_json_helper_class_obj = JsonHelpers()
            __local_json_first_child_label_list =__local_json_helper_class_obj.get_first_col_value(json_data)
            # comparing lists from application and json files
            if len(__local_json_first_child_label_list) == len(Test_Functional.col1_label_value):
                assert Test_Functional.col1_label_value == __local_json_first_child_label_list
            else:
                raise("Values in the first column are not matching.Test case is failed")
        except Exception as e:
            self.log.exception("Exception ####  {}".format(e))
            pytest.fail(e)
    #
    # def test_3_sample(self):
    #     assert False
#
# ###################################################################################################################################
# # Validate images and children for a selected category
# ###################################################################################################################################
#
    def test_4_validate_images_and_children_for_each_category(self,json_data):
        __local_tbm_page_obj = tbmpage()
        try:
            __local_tbm_page_obj.validate_cloud_details_images_and_children_for_category(json_data,Test_Functional.col1_id_value)
            results = getattr(__local_tbm_page_obj,"child_validation_results")
            #pdb.set_trace()
            val = [d["Key_value"] for d in results if d["FinalStatus"] == "Fail"]  # get the list of failed values from the results collected
            Apptio_Common.write_category_details_to_csv("ChildrenValidationResults",Constant_Values.children_validation_col_list,results) # write all the results in csv
            if len(val)>0: # if the length of failed list is > 0 , then fail the test case
                pytest.fail("Test case is failed")
        except Exception as e:
            self.log.exception("Exception #####  {}".format(e))
            raise
# #####################################################################################################################################
# # Validate details of a category
# #####################################################################################################################################
#
#     def test_5_validate_details_of_each_category(self, json_data):
#         __local_tbm_page_obj = tbmpage()
#         try:
#             __local_tbm_page_obj.validate_details_of_each_category_in_columns(json_data,Test_Functional.col1_id_value,Test_Functional.col1_label_value)
#             results_list = getattr(Apptio_Common,"details_results_list")
#             Apptio_Common.write_category_details_to_csv("CategoryDetailsResults",Constant_Values.detail_validation_col_list,results_list)
#             fail_list = [d for d in results_list if d["Status"] =="Fail" ]
#             if len(fail_list) >0:
#                 pytest.fail("Test case is failed")
#             setattr(Apptio_Common,"details_results_list",[])
#         except Exception as e:
#             self.log.exception("Exception #####  {}".format(e))
#             raise
#
# #####################################################################################################################################
# # Validate include and exclude values
# #####################################################################################################################################
#
#     def test_6_validate_include_and_exclude_details_of_each_category(self, json_data):
#         __local_tbm_page_obj = tbmpage()
#         try:
#             __local_tbm_page_obj.validate_exclude_and_include_of_each_category(json_data,Test_Functional.col1_id_value,Test_Functional.col1_label_value)
#             results_list = getattr(Apptio_Common, "details_results_list")
#             Apptio_Common.write_category_details_to_csv("IncludesandExcludesResults", Constant_Values.detail_validation_col_list, results_list)
#             fail_list = [d for d in results_list if d["Status"] == "Fail"]
#             if len(fail_list) > 0:
#                 pytest.fail("Test case is failed")
#             setattr(Apptio_Common,"details_results_list",None)
#         except Exception as e:
#             self.log.exception("Exception #####  {}".format(e))
#             pytest.fail(e)
#
#


#####################################################################################################################################
# Logout from application
#####################################################################################################################################
    def test_7_Logout_from_application(self):
        try:
            obj_login_page = LoginPage()
            obj_login_page.logout()
        except Exception as e:
            self.log.exception("Exception #####  {}".format(e))
            pytest.fail(e)

########################################################################################################################
########################################################################################################################