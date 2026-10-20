Celem zadania jest zapoznanie się ze strukturą plików medycznych DICOM oraz metadanymi zawartymi w nagłówku. Należy przygotować prostą przeglądarkę obrazów DICOM w Pythonie (np. z użyciem bibliotek pydicom, matplotlib, opencv lub tkinter).

Użytkownik wskazuje plik DICOM (.dcm) z dysku.
Program poprawnie wczytuje dane obrazu.
Obraz wyświetlany jest w oknie. Użytkownik może powiększać obraz oraz przesuwać. Przy dużym powiększeniu gdy widać pojedyncze piksele, to na pikselach pojawia się napis z wartością piksela (np. 128, 128, 128 w przypadku RGB, albo np. 256 w przypadku obrazu 8-bit odcienie szarości).
W przypadku wielowarstwowych badań (np. tomografia) można przeglądać poszczególne warstwy (np. z menu albo klawiszami ↑ ↓).
Program w osobnym panelu pokazuje metadane z nagłówka DICOM, np. PatientName, PatientID, StudyDate, Modality, Rows, Columns, PixelSpacing, SliceThickness, etc. Uwaga: nie wszystkie dane mogą być w pliku dostępne, idealnie jakby program wyświetlał wszystkie niepuste metadane.
Opcjonalnie na ocenę 5.0: obsługa folderu z wieloma plikami DICOM (np. całe badanie CT)