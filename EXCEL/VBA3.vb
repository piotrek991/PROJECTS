Option Explicit

Sub wth_change_font()
    Dim myrange As Range
    Set myrange = Range("A10", "A" & Cells(Rows.Count, 1).End(xlUp).Row)
    Debug.Print myrange.Address
    With myrange.Font
        .name = "Arial"
        .Size = 12
        .Bold = True
    End With
    
End Sub

Sub wth_Reset_font()
    Dim myrange As Range
    Set myrange = Range("A10", "A" & Cells(Rows.Count, 1).End(xlUp).Row)
    Debug.Print myrange.Address
    With myrange.Font
        .name = "Calibri"
        .Size = 11
        .Bold = False
    End With
    
End Sub

Sub protect_all_sheets()
    Dim sh As Worksheet
    For Each sh In ThisWorkbook.Worksheets
        sh.Protect Password:="test", AllowFormattingCells:=True, AllowFormattingColumns:=True, _
        AllowFormattingRows:=True
        
    Next sh


End Sub

Sub unprotect_all_sheets()
    Dim sh As Worksheet
    For Each sh In ThisWorkbook.Worksheets
        sh.Unprotect "test"
    Next sh


End Sub

Sub simple_if()
If Range("B4").Value <> "" Then
    Range("C3").Value = Range("B3").Value
End If

If Range("B4").Value >= 0 And Range("B4").Value <= 400 Then
    Range("C4").Value = Range("B4").Value
End If

End Sub

Sub protect_sheets_but()
Dim sh As Worksheet
    For Each sh In Worksheets
        If sh.name <> "Purpose" Then
            sh.Protect Password:="test", AllowFormattingCells:=True
        Else
            sh.Protect Password:="test"
        End If
        
    Next sh
End Sub

Sub count_formulas()
 Dim cell As Range, how_many As Integer
 
 For Each cell In Range("A8", "B9")
    If cell.HasFormula = True Then
        how_many = how_many + 1
    End If
 Next cell
 Debug.Print how_many
 
End Sub

Sub top_3()
Dim IntRange As Range, cell As Range
Dim final_text As String
Dim max_1 As Integer, max_2 As Integer, max_3 As Integer

Set IntRange = Excel.Application.InputBox("Select a range to get top 3 Values", "Top3", , , , , , 8)
max_1 = Excel.WorksheetFunction.Max(IntRange)
For Each cell In IntRange
    If cell.Value > max_2 And cell.Value < max_1 Then
        max_3 = max_2
        max_2 = cell.Value
    ElseIf cell.Value > max_3 And cell.Value < max_2 Then
        max_3 = cell.Value
    End If
Next cell
final_text = "Top 1 = " & max_1 & vbNewLine & _
"Top 2 = " & max_2 & vbNewLine & _
"Top 3 = " & max_3 & ""
MsgBox (final_text)

End Sub

Sub fill_100k()
Dim cell As Range
Dim shNew As Worksheet

Set shNew = Worksheets.Add
shNew.name = "SLOW"
For Each cell In shNew.Range("A1:A100000")
    cell.Value = Excel.WorksheetFunction.RandBetween(0, 100)
Next cell

End Sub

Sub create_table_contest()
Dim cell As Range
Dim sh As Worksheet
Dim CurrName As String
Set cell = Excel.Application.InputBox("Gdzie chcesz umieścić spis treści" & vbNewLine & "Proszę wskaż komórkę :", "Wprowadź Spis Treści", , , , , , 8)
Set cell = cell.Cells(1, 1)

For Each sh In ThisWorkbook.Worksheets
    cell.Value = sh.name
    Set cell = cell.Offset(1, 0)
Next sh
End Sub

Sub multiple_find()
Dim compid As Range
Dim first_find As Long
Range("D3").ClearContents

Set compid = Range("A:A").Find(Range("B3").Value, , xlValues, xlWhole)
If compid Is Nothing Then
    MsgBox ("Theres no matches")
    Exit Sub
End If

first_find = compid.Row
 Do
    Range("D3").Value = Range("D3").Value & compid.Offset(0, 4).Value & vbNewLine
    Set compid = Range("A:A").FindNext(compid)
    If compid.Row = first_find Then Exit Do
Loop

End Sub
Sub find_all_comments()
    Dim cell As Range, shNew As Worksheet, last_row As Long
    If find_sheet("Comments") = False Then
        Set shNew = Sheets.Add(After:=Sheets(Sheets.Count))
        shNew.name = "Comments"
        shNew.Activate
        Range("A1").Value = "Comment"
        Range("B1").Value = "Addres"
        Range("C1").Value = "Author"
    End If
    For Each Worksheet In ThisWorkbook.Sheets
        Worksheet.Activate
        For Each cell In Range("A1:G100")
            If Worksheet.name <> "Comments" Then
                If Not cell.Comment Is Nothing Then
                    Sheets("Comments").Activate
                    last_row = Range("A1").CurrentRegion.Rows.Count + 1
                    Range("A" & last_row) = Worksheet.name & "!" & cell.Comment.Text
                    Range("B" & last_row) = Worksheet.name & "!" & cell.Address
                    Range("C" & last_row) = Worksheet.name & "!" & cell.Comment.Author
                End If
            End If
        Next cell
    Next Worksheet
End Sub

Function find_sheet(name As String) As Boolean
    For Each Worksheet In ThisWorkbook.Worksheets
        If Worksheet.name = name Then
           find_sheet = True
           Exit Function
        End If
    Next Worksheet
    find_sheet = False
End Function








V 