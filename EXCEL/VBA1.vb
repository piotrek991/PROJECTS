Sub create_workbook_for_each_company()
    Dim start_cell  As Long, last_cell As Long
    Dim new_workbook As Workbook
    Dim workbook_name As String, path As String
    path = "C:\Users\48511\Documents\KURSY_resources\VBA_COURSE\SKOROSZYTY\"
    start_cell = 7
    last_cell = Range("A" & start_cell).End(xlDown).Row
    Dim tab_c_m(1 To 8, 1 To 2) As String
    
    On Error GoTo leave
    For r = start_cell To last_cell
        For c = 1 To 2
            tab_c_m(r - start_cell + 1, c) = Range("A" & r).Offset(0, c - 1).Value
            If c = 1 Then
                Set new_workbook = Workbooks.Add
                workbook_name = tab_c_m(r - start_cell + 1, c) & ".xlsm"
                ActiveWorkbook.SaveAs filename:=path & workbook_name, FileFormat:=xlOpenXMLWorkbookMacroEnabled
                ActiveWorkbook.Sheets("Arkusz1").Range("A1").Value = tab_c_m(r - start_cell + 1, c)
                ActiveWorkbook.Close (True)
            Else
                Workbooks.Open (path & workbook_name)
                ActiveWorkbook.Sheets("Arkusz1").Range("A2").Value = tab_c_m(r - start_cell + 1, c)
                ActiveWorkbook.Close (True)
            End If
            Workbooks("S11_arrays_Start.xlsm").Activate
        Next c
    Next r
    leave:
End Sub