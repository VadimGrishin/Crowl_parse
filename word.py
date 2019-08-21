import win32com.client  # pip install pywin32

w = win32com.client.gencache.EnsureDispatch('Word.Application')
word = win32com.client.DispatchEx("Word.Application")

word.Visible = True
word.DisplayAlerts = 0
word.Documents.Open("C:\\Users\\Vadim Grishin\\parsing\\less8\\data\\reglaments\\r1_01082019_02082019.docx")
print(1)
# print(list(win32com.client.constants))
# find = word.Selection.Find
# find.Text = "утвержден 26 ноября 2009 года "
# find.Replacement.Text = "John"
# find.Execute(Replace=1, Forward=True)
#
# # the following part doesn't run
# find.Text = "Last Name"
# find.Replacement.Text = "Smith"
# find.Execute(Replace=1, Forward=True)



word.ActiveDocument.SaveAs("C:/Users/Vadim Grishin/parsing/less8/data/reglaments/r1_999.txt",
                           FileFormat=win32com.client.constants.wdFormatText)
word.Quit() # releases Word object from memory