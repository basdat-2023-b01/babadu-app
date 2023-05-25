from django import forms

class BuatUjianKualifikasi(forms.Form):
    tahun = forms.CharField(
        label='tahun',
        min_length=1,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'tahun', 'placeholder': 'YYYY'})
    )
    batch = forms.CharField(
        label='batch',
        min_length=1,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'batch', 'placeholder': 'Nomor Batch'})
    )
    tempat_pelaksanaan = forms.CharField(
        label='tempat pelaksanaan',
        min_length=1,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'tempat-pelaksanaan', 'placeholder': 'Tempat Pelaksanaan'})
    )
    tanggal_pelaksanaan = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class PertanyaanKualifikasiForm(forms.Form):
    PILIHAN_NOMOR_SATU = [
        ('0', 'China'),
        ('20', 'Britain'),
        ('0', 'Denmark'),
    ]
    nomor_satu = forms.CharField(
        label='satu',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_SATU
        )
    )
    PILIHAN_NOMOR_DUA = [
        ('0', '11'),
        ('0', '16'),
        ('20', '21'),
    ]
    nomor_dua = forms.CharField(
        label='dua',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_DUA
        )
    )
    PILIHAN_NOMOR_TIGA = [
        ('20', 'Badminton World Federation – BWF'),
        ('0', 'International Badminton Association – IBA'),
        ('0', 'Badminton World Organization – BWO'),
    ]
    nomor_tiga = forms.CharField(
        label='tiga',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_TIGA
        )
    )
    PILIHAN_NOMOR_EMPAT = [
        ('0', 'Before the game starts'),
        ('0', 'After the game finishes'),
        ('20', 'After the rally finishes'),
    ]
    nomor_empat = forms.CharField(
        label='empat',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_EMPAT
        )
    )
    PILIHAN_NOMOR_LIMA = [
        ('0', 'Error'),
        ('20', 'Fault'),
        ('0', 'Mistake'),
    ]
    nomor_lima = forms.CharField(
        label='lima',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_LIMA
        )
    )