import mysql.connector
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", # ako niste nista menjali u phpmyadminu ovo su standardni
    # username i password
	database="g2" # iz phpmyadmin 
    )

class Korisnik:
    __id:int
    __index:str
    __email:str
    __ime_prezime:str
    __sifra:str
    __godina_rodjenja:int


    def __init__(self, id, index, email, ime_prezime,sifra,godina_rodjenja) -> None:
        self.__id=id
        self.__index=index
        self.__email=email
        self.__ime_prezime=ime_prezime
        self.__sifra=sifra
        self.__godina_rodjenja=godina_rodjenja

    def __str__(self) -> str:
        rez=f"ID:{self.__id}\n"
        rez+=f'Index:{self.__index}\n'
        rez+=f'email:{self.__email}\n'
        rez+=f'ime_prezime:{self.__ime_prezime}\n'
        rez+=f'sifra:{self.__sifra}\n'
        rez+=f'godina_rodjenja:{self.__godina_rodjenja}'

        return rez

    def get_id(self):
        return self.__id

    def get_index(self):
        return self.__index

    def get_email(self):
        return self.__email

    def get_ime_prezime(self):
        return self.__ime_prezime
    def get_sifra(self):
        return self.__sifra

    def get_godina_rodjenja(self):
        return self.__godina_rodjenja

    def set_id(self, novi_id):
        self.__id=novi_id

    def set_index(self, novi_index):
        self.__index=novi_index

    def set_email(self, novi_email):
        if "@" not in novi_email:
            print("Email mora sadrzati @")
            return

        self.__email=novi_email

    def set_sifra(self, nova_sifra):
        if len(nova_sifra)<3:
            print("sifra mora imati makar 3 karaktera")
            return

        self.__sifra=nova_sifra

    def set_godina_rodjenja(self,nova_godina):
        self.__godina_rodjenja=nova_godina

    @staticmethod
    def insert(index,email,ime_prezime,sifra,godina_rodjenja):
        cursor=mydb.cursor(prepared=True)
        sql="insert into g2 values(null, ?,?,?,?,?)"
        parametri=(index,email,ime_prezime,sifra,godina_rodjenja)
        cursor.execute(sql,parametri)
        mydb.commit()

    @staticmethod
    def dohvati_korisnika(index):
        cursor=mydb.cursor(prepared=True)
        sql="select * from g2 where indeks=?"
        parametri=(index,)
        cursor.execute(sql, parametri)
        rezultat=cursor.fetchone()

        if rezultat==None:
            return None
        
        rezultat=Korisnik.dekodiraj_tapl(rezultat)
        korisnik=Korisnik.korisnik_od_reda(rezultat)

        return korisnik


    @staticmethod
    def dekodiraj_tapl(tapl):
        tapl=list(tapl)
        n=len(tapl)
        for i in range(n):
            if isinstance(tapl[i],bytearray):
                tapl[i]=tapl[i].decode()

        return tapl
    
    @staticmethod
    def dekodiraj_listu_taplova(lista_taplova):
        n=len(lista_taplova)
        for i in range(n):
            lista_taplova[i]=Korisnik.dekodiraj_tapl(lista_taplova[i])

        return lista_taplova

    @classmethod
    def korisnik_od_reda(cls,red):
        id, index,email,ime_prezime,sifra,godina_rodjenja=red
        return cls(id, index,email,ime_prezime,sifra,godina_rodjenja)

    @staticmethod
    def korisnici_od_liste_redova(lista_redova):
        korisnici=[]
        for red in lista_redova:
            korisnik=Korisnik.korisnik_od_reda(red)
            korisnici.append(korisnik)

        return korisnici

    @staticmethod
    def dohvati_sve_korisnike():
        cursor=mydb.cursor(prepared=True)
        sql='select * from g2'
        cursor.execute(sql)
        rezultat=cursor.fetchall()
        rezultat=Korisnik.dekodiraj_listu_taplova(rezultat)
        korisnici=Korisnik.korisnici_od_liste_redova(rezultat)
        return korisnici

    @staticmethod
    def update(email,ime_prezime,godina_rodjenja, index):
        cursor=mydb.cursor(prepared=True)
        sql="update g2 set email=?,ime_prezime=?, godina=? where indeks=?" 
        parametri=(email,ime_prezime,godina_rodjenja,index)
        cursor.execute(sql, parametri)
        mydb.commit()
        
    @staticmethod
    def stariji_od(godiste):
        cursor=mydb.cursor(prepared=True)
        sql=f"select * from g2 where godina<{godiste}"
        cursor.execute(sql)
        rezultat=cursor.fetchall()
        if rezultat==[]:
            return None
        rezultat=Korisnik.dekodiraj_listu_taplova(rezultat)
        korisnici=Korisnik.korisnici_od_liste_redova(rezultat)

        return korisnici

        