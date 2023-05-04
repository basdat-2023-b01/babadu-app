from django import forms

class DataKualifikasiForm(forms.Form):
    TEMPAT_PELAKSANAAN = [
        ('1', 'Indonesia'),
        ('2', 'Jepang'),
        ('3', 'Korea'),
        ('4', 'China'),
        ('5', 'Thailand'),
    ]
    TANGGAL_PELAKSANAAN = [
        ('1', '2016-03-26'),
        ('2', '2017-05-11'),
        ('3', '2018-08-28'),
        ('4', '2019-09-10'),
        ('5', '2020-11-22'),
    ]
    nomor_batch = forms.CharField(
        label='nomor batch',
        min_length=1,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'nomor-batch', 'placeholder': 'Nomor Batch'})
    )
    tempat_pelaksanaan = forms.CharField(
        label='tempat pelaksanaan',
        widget=forms.Select(
            choices=TEMPAT_PELAKSANAAN
        )
    )
    tanggal_pelaksanaan = forms.CharField(
        label='tanggal pelaksanaan',
        widget=forms.Select(
            choices=TANGGAL_PELAKSANAAN
        )
    )

class PertanyaanKualifikasiForm(forms.Form):
    PILIHAN_NOMOR_SATU = [
        ('1', 'China'),
        ('2', 'Britain'),
        ('3', 'Denmark'),
    ]
    nomor_satu = forms.CharField(
        label='satu',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_SATU
        )
    )
    PILIHAN_NOMOR_DUA = [
        ('1', '11'),
        ('2', '16'),
        ('3', '21'),
    ]
    nomor_dua = forms.CharField(
        label='dua',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_DUA
        )
    )
    PILIHAN_NOMOR_TIGA = [
        ('1', 'Badminton World Federation – BWF'),
        ('2', 'International Badminton Association – IBA'),
        ('3', 'Badminton World Organization – BWO'),
    ]
    nomor_tiga = forms.CharField(
        label='tiga',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_TIGA
        )
    )
    PILIHAN_NOMOR_EMPAT = [
        ('1', 'Before the game starts'),
        ('2', 'After the game finishes'),
        ('3', 'After the rally finishes'),
    ]
    nomor_empat = forms.CharField(
        label='empat',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_EMPAT
        )
    )
    PILIHAN_NOMOR_LIMA = [
        ('1', 'Error'),
        ('2', 'Fault'),
        ('3', 'Mistake'),
    ]
    nomor_lima = forms.CharField(
        label='lima',
        widget=forms.RadioSelect(
            choices=PILIHAN_NOMOR_LIMA
        )
    )