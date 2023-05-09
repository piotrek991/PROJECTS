Sub create_text_file()
    Dim filename As String, path As String, text_to_write As String
    Dim start_row As Long, last_row As Long, last_column As Long
    
    path = ThisWorkbook.path
    filename = path & "\Project_activity_s12.csv"
    start_row = 6
    last_row = Range("A" & start_row).End(xlDown).Row
    last_column = Range("A" & start_row).End(xlToRight).Column
    
    Open filename For Output As #1
    For r = start_row To last_row
        For c = 0 To last_column - 1
            If c <> last_column - 1 Then
                text_to_write = text_to_write & Range("A" & start_row).Offset(r - start_row, c).Value & ";"
            Else
                text_to_write = text_to_write & Range("A" & start_row).Offset(r - start_row, c).Value
            End If
        Next c
        Print #1, text_to_write
        text_to_write = ""
    Next r
    Close #1
End Sub
