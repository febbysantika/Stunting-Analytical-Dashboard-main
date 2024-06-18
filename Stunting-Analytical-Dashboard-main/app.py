import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import xlsxwriter

from io import BytesIO
from st_aggrid import AgGrid
from PIL import Image

# st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Stunting Tester",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Database
conn = sqlite3.Connection('data.db')
c = conn.cursor()

def create_table_ibu():
    c.execute('CREATE TABLE IF NOT EXISTS ibutable(ibu_kia TEXT,ibu_nama TEXT,ibu_status_kehamilan TEXT,ibu_perkiraan_tanggal_lahir DATE,ibu_usia_kehamilan TEXT,ibu_tanggal_melahirkan DATE,ibu_pemeriksaan TEXT,ibu_konsumsi TEXT,ibu_nifas TEXT,ibu_gizi TEXT,ibu_kunjungan TEXT,ibu_air_bersih TEXT,ibu_jamban TEXT,ibu_jakes TEXT)')
    
def create_table_anak():
    c.execute('CREATE TABLE IF NOT EXISTS anaktable(anak_kia TEXT,anak_nama TEXT,anak_kelamin TEXT,anak_tl TEXT,anak_gizi TEXT,anak_umur TEXT,anak_hasil TEXT,anak_imun_dasar TEXT,anak_bb TEXT,anak_tb TEXT,anak_konseling_l TEXT,anak_konseling_p TEXT,anak_kunjungan TEXT,anak_air TEXT,anak_jamban TEXT,anak_akta TEXT,anak_jakes TEXT,anak_paud TEXT)')

def add_data_ibu(ibu_kia,ibu_nama,ibu_status_kehamilan,ibu_perkiraan_tanggal_lahir,ibu_usia_kehamilan,ibu_tanggal_melahirkan,ibu_pemeriksaan,ibu_konsumsi,ibu_nifas,ibu_gizi,ibu_kunjungan,ibu_air_bersih,ibu_jamban,ibu_jakes):
    c.execute('INSERT INTO ibutable(ibu_kia,ibu_nama,ibu_status_kehamilan,ibu_perkiraan_tanggal_lahir,ibu_usia_kehamilan,ibu_tanggal_melahirkan,ibu_pemeriksaan,ibu_konsumsi,ibu_nifas,ibu_gizi,ibu_kunjungan,ibu_air_bersih,ibu_jamban,ibu_jakes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (ibu_kia,ibu_nama,ibu_status_kehamilan,ibu_perkiraan_tanggal_lahir,ibu_usia_kehamilan,ibu_tanggal_melahirkan,ibu_pemeriksaan,ibu_konsumsi,ibu_nifas,ibu_gizi,ibu_kunjungan,ibu_air_bersih,ibu_jamban,ibu_jakes))
    conn.commit()
    
def add_data_anak(anak_kia,anak_nama,anak_kelamin,anak_tl,anak_gizi,anak_umur,anak_hasil,anak_imun_dasar,anak_bb,anak_tb,anak_konseling_l,anak_konseling_p,anak_kunjungan,anak_air,anak_jamban,anak_akta,anak_jakes,anak_paud):
    c.execute('INSERT INTO anaktable(anak_kia,anak_nama,anak_kelamin,anak_tl,anak_gizi,anak_umur,anak_hasil,anak_imun_dasar,anak_bb,anak_tb,anak_konseling_l,anak_konseling_p,anak_kunjungan,anak_air,anak_jamban,anak_akta,anak_jakes,anak_paud) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (anak_kia,anak_nama,anak_kelamin,anak_tl,anak_gizi,anak_umur,anak_hasil,anak_imun_dasar,anak_bb,anak_tb,anak_konseling_l,anak_konseling_p,anak_kunjungan,anak_air,anak_jamban,anak_akta,anak_jakes,anak_paud))
    conn.commit()
    
def view_data_ibu():
    c.execute('SELECT * FROM ibutable')
    data_ibu = c.fetchall()
    return data_ibu 

def view_data_anak():
    c.execute('SELECT * FROM anaktable')
    data_anak = c.fetchall()
    return data_anak

def delete_data_ibu(ibu_kia):
    c.execute('DELETE FROM ibutable where ibu_kia="{}"'.format(ibu_kia))
    conn.commit()
    
def delete_data_anak(anak_kia):
    c.execute('DELETE FROM anaktable where anak_kia="{}"'.format(anak_kia))
    conn.commit()
    
        
def main():
    st.title('Stunting Tester')
    menu = ["🏠 Home", "📊 Dashboard", "🤰 Pemantauan Ibu Hamil", "👶 Pemantauan Bulanan Anak"]
    st.sidebar.title('👇 Silakan Pilih Menu')
    choice = st.sidebar.selectbox("Menu", menu)
    st.sidebar.markdown('**This app is still in development mode**')
    
    if choice == "🏠 Home":
        st.subheader("🏠 Home")
        image_home = Image.open('Images/stunt.jpeg')
        st.image(image_home, width = 1000)
        
    elif choice == "📊 Dashboard":
        st.subheader("📊 Dashboard")
        result_ibu = view_data_ibu()
        result_anak = view_data_anak()
        clean_db_ibu = pd.DataFrame(result_ibu, columns = ['No Register (KIA)', 'Nama Ibu', 'Status Kehamilan (KEK/RISTI)',
                                                        'Hari Perkiraan Lahir (Tgl/Bln/Thn)','Usia Kehamilan (Bulan)',
                                                        'Tanggal Melahirkan  (Tgl/Bln/Thn)', 'Pemeriksaan Kehamilan',
                                                        'Dapat & Konsumsi Pil Fe', 'Pemeriksaan Nifas', 'Konseling Gizi (Kelas IH)',
                                                        'Kunjungan Rumah', 'Kepemilikan Akses Air Bersih', 'Kepemilikan Jamban',
                                                        'Jaminan Kesehatan'])
        
        clean_db_anak = pd.DataFrame(result_anak, columns = ['No Register','Nama Anak','Jenis Kelamin','Tanggal Lahir',
                                                            'Status Gizi Anak','Umur (Bulan)','Hasil','Pemberian Imunisasi Dasar',
                                                            'Pengukuran Berat Badan','Pengukuran Tinggi Badan',
                                                            'Konseling Gizi Bagi Orang Tua (L)','Konseling Gizi Bagi Orang Tua (P)',
                                                            'Kunjungan Rumah','Kepemilikan Akses Air Bersih','Kepemilikan Jamban Sehat',
                                                            'Akta Lahir','Jaminan Kesehatan','Pengasuhan (PAUD)'])

        tab1, tab2 = st.tabs(["Data", "Visualization"])

        with tab1:
            # Total RT
            total_ibu = clean_db_ibu.shape[0]
            # Total Anak
            total_anak = clean_db_anak.shape[0]
            # Total RISTI
            total_hamil = clean_db_ibu['Status Kehamilan (KEK/RISTI)'].value_counts()
            total_hamil_resti = total_hamil.loc['RISTI']
            # Total Rumah Tangga Rentan
            
            # Total Anak Gizi Kurang
            total_anak2 = clean_db_anak['Status Gizi Anak'].value_counts()
            total_anak_kurang = total_anak2.loc['Kurang']
            # Total Anak Gizi Buruk
            total_anak_buruk = total_anak2.loc['Buruk']
            # Total Anak Stunting
            total_anak_stunting = total_anak2.loc['Stunting']
            
            # Total Air Tidak Bersih
            total_air_ibu = clean_db_ibu['Kepemilikan Akses Air Bersih'].value_counts()
            total_air_ibu_tidak = total_air_ibu.loc['Tidak']
            total_air_anak = clean_db_anak['Kepemilikan Akses Air Bersih'].value_counts()
            total_air_anak_tidak = total_air_anak.loc['Tidak']
            total_air_tidak_bersih = total_air_ibu_tidak + total_air_anak_tidak
            
            # Total Tidak Punya Jamban
            total_jamban_ibu = clean_db_ibu['Kepemilikan Jamban'].value_counts()
            total_jamban_ibu_tidak = total_jamban_ibu.loc['Tidak']
            total_jamban_anak = clean_db_anak['Kepemilikan Jamban Sehat'].value_counts()
            total_jamban_anak_tidak = total_jamban_anak.loc['Tidak']
            total_tidak_jamban = total_jamban_ibu_tidak + total_jamban_anak_tidak
            
            # Total Ibu Tidak Mempunyai Jakes
            total_ibu_jakes = clean_db_ibu['Jaminan Kesehatan'].value_counts()
            total_ibu_jakes_tidak = total_ibu_jakes.loc['Tidak']

            # Total Anak Tidak Mempunyai Jakes
            total_anak_jakes = clean_db_anak['Jaminan Kesehatan'].value_counts()
            total_anak_jakes_tidak = total_anak_jakes.loc['Tidak']        
            
            # Total Anak Tidak Mempunyai Akta Lahir
            total_anak_akta = clean_db_anak['Akta Lahir'].value_counts()
            total_anak_akta_tidak = total_anak_akta.loc['Tidak']  
                    
            # Metric
            st.markdown("""
                        <style>
                        div[data-testid="metric-container"] {
                        background-color: rgba(28, 131, 225, 0.1);
                        border: 1px solid rgba(28, 131, 225, 0.1);
                        padding: 5% 5% 5% 10%;
                        border-radius: 5px;
                        color: rgb(71, 198, 218);
                        overflow-wrap: break-word;
                        }

                        /* breakline for metric text         */
                        div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
                        overflow-wrap: break-word;
                        white-space: break-spaces;
                        color: white;
                        }
                        </style>
                        """
                        , unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Rumah Tangga Sasaran", total_ibu)
            col2.metric("Rumah Tangga Kategori Rentan", "9")
            col3.metric("Ibu Hamil Resti", total_hamil_resti)
            col4.metric("Anak 0 - 23 Bulan", total_anak)

            col1, col2, col3= st.columns(3)
            col1.metric("Anak 0 - 23 Bulan Kondisi Gizi Kurang", total_anak_kurang)
            col2.metric("Anak 0 - 23 Bulan Kondisi Gizi Buruk", total_anak_buruk)
            col3.metric("Anak 0 - 23 Bulan Terindikasi Stunting", total_anak_stunting)
            
            col1, col2= st.columns(2)
            col1.metric("Rumah Tangga Tidak Memiliki Sumber Air Bersih Layak Minum", total_air_tidak_bersih)
            col2.metric("Rumah Tangga Tidak Mempunyai Jamban", total_tidak_jamban)
            
            col1, col2, col3= st.columns(3)
            col1.metric("Ibu Hamil Tidak Mempunyai Jaminan Kesehatan", total_ibu_jakes_tidak)
            col2.metric("Anak 0 - 23 Bulan Tidak Mempunyai Jaminan Kesehatan", total_anak_jakes_tidak)
            col3.metric("Anak 0 - 23 Bulan Tidak Mempunyai Akta Kelahiran", total_anak_akta_tidak)

        with tab2:
            st.subheader("Status Gizi Anak")
            metrics_anak = clean_db_anak
            ax = sns.countplot(data = metrics_anak, x = 'Status Gizi Anak')
            for container in ax.containers:
                ax.bar_label(container)
            st.pyplot(transparent=True)



        
    elif choice == "🤰 Pemantauan Ibu Hamil":
        st.subheader("🤰 Pemantauan Ibu Hamil")
        menu_3 = ["Data Ibu Hamil", "Data Visualization", "Tambah Data Ibu Hamil"]
        choice_3 = st.selectbox("Menu", menu_3)
        
        if choice_3 == "Data Ibu Hamil":
            st.subheader("Data Ibu Hamil")
            result = view_data_ibu()
            clean_db_ibu = pd.DataFrame(result, columns = ['No Register (KIA)', 'Nama Ibu', 'Status Kehamilan (KEK/RISTI)',
                                                        'Hari Perkiraan Lahir (Tgl/Bln/Thn)','Usia Kehamilan (Bulan)',
                                                        'Tanggal Melahirkan  (Tgl/Bln/Thn)', 'Pemeriksaan Kehamilan',
                                                        'Dapat & Konsumsi Pil Fe', 'Pemeriksaan Nifas', 'Konseling Gizi (Kelas IH)',
                                                        'Kunjungan Rumah', 'Kepemilikan Akses Air Bersih', 'Kepemilikan Jamban',
                                                        'Jaminan Kesehatan'])
            AgGrid(clean_db_ibu)
            
            st.download_button("Download Data Ibu", clean_db_ibu.to_csv(),file_name = 'data_ibu.csv', mime = 'text/csv')
            
            # Delete data
            st.subheader('Hapus Data')
            no_register_ibu = [i[0] for i in view_data_ibu()]
            delete_data_by_no_register = st.selectbox("Nomor Register (KIA)", no_register_ibu)
            
            if st.button("Hapus Data"):
                delete_data_ibu(delete_data_by_no_register)
                st.warning("Data : '{}'".format(delete_data_by_no_register))
                
        if choice_3 == "Data Visualization":
            st.subheader("Data Visualization")
            result = view_data_ibu()
            clean_db_ibu = pd.DataFrame(result, columns = ['No Register (KIA)', 'Nama Ibu', 'Status Kehamilan (KEK/RISTI)', 
                                                        'Hari Perkiraan Lahir (Tgl/Bln/Thn)','Usia Kehamilan (Bulan)', 
                                                        'Tanggal Melahirkan  (Tgl/Bln/Thn)', 'Pemeriksaan Kehamilan', 
                                                        'Dapat & Konsumsi Pil Fe', 'Pemeriksaan Nifas', 'Konseling Gizi (Kelas IH)', 
                                                        'Kunjungan Rumah', 'Kepemilikan Akses Air Bersih', 'Kepemilikan Jamban', 
                                                        'Jaminan Kesehatan'])
            plt.style.use('dark_background')
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Status Kehamilan")
                metrics_ibu = clean_db_ibu
                metrics_ibu['Status Kehamilan (KEK/RISTI)'].value_counts().plot(kind='barh')
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Usia Kehamilan")
                metrics_ibu['Usia Kehamilan (Bulan)'].value_counts().plot.pie()
                st.pyplot(transparent=True)

            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pemeriksaan Kehamilan")
                metrics_ibu = clean_db_ibu
                ax = sns.countplot(data = metrics_ibu, x = 'Pemeriksaan Kehamilan', orient = 'h')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Dapat & Konsumsi Pil Fe")
                ax = sns.countplot(data = metrics_ibu, x = 'Dapat & Konsumsi Pil Fe')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)  
                
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Hari Perkiraan Lahir (Tgl/Bln/Thn)")
                metrics_ibu = clean_db_ibu
                metrics_ibu['Hari Perkiraan Lahir (Tgl/Bln/Thn)'].value_counts().plot(kind='line')
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Tanggal Melahirkan  (Tgl/Bln/Thn)")
                metrics_ibu['Tanggal Melahirkan  (Tgl/Bln/Thn)'].value_counts().plot(kind='line')
                st.pyplot(transparent=True)
            
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pemeriksaan Nifas")
                metrics_ibu = clean_db_ibu
                ax = sns.countplot(data = metrics_ibu, x = 'Pemeriksaan Nifas')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Konseling Gizi (Kelas IH)")
                ax = sns.countplot(data = metrics_ibu, x = 'Konseling Gizi (Kelas IH)')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)  
            
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Kunjungan Rumah")
                metrics_ibu = clean_db_ibu
                ax = sns.countplot(data = metrics_ibu, x = 'Kunjungan Rumah')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Kepemilikan Akses Air Bersih")
                ax = sns.countplot(data = metrics_ibu, x = 'Kepemilikan Akses Air Bersih')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True) 
            
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Kepemilikan Jamban")
                metrics_ibu = clean_db_ibu
                ax = sns.countplot(data = metrics_ibu, x = 'Kepemilikan Jamban')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Jaminan Kesehatan")
                ax = sns.countplot(data = metrics_ibu, x = 'Jaminan Kesehatan')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True) 
                        
        if choice_3 == "Tambah Data Ibu Hamil":
            st.subheader("Tambah Data Ibu Hamil")
            create_table_ibu()
            
            # Tambah data ibu
            ibu_kia = st.text_input('Masukkan No Register')
            ibu_nama = st.text_input('Masukkan Nama Ibu')
            ibu_status_kehamilan = option = st.selectbox('Status Kehamilan', ('Normal', 'KEK', 'RISTI'))
            ibu_perkiraan_tanggal_lahir = st.date_input('Masukkan Hari Perkiraan Lahir')
            ibu_usia_kehamilan = st.text_input('Masukkan Usia Kehamilan')
            ibu_tanggal_melahirkan = st.date_input('Masukkan Tanggal Melahirkan')
            ibu_pemeriksaan = option = st.selectbox('Pemeriksaan Kehamilan', ('Iya', 'Tidak'))
            ibu_konsumsi = option = st.selectbox('Dapat & Konsumsi Pil Fe', ('Iya', 'Tidak'))
            ibu_nifas = option = st.selectbox('Pemeriksaan Nifas', ('Iya', 'Tidak'))
            ibu_gizi = option = st.selectbox('Konseling Gizi (Kelas IH)', ('Iya', 'Tidak'))
            ibu_kunjungan = option = st.selectbox('Kunjungan Rumah', ('Iya', 'Tidak'))
            ibu_air_bersih = option = st.selectbox('Kepemilikan Akses Air Bersih', ('Iya', 'Tidak'))
            ibu_jamban = option = st.selectbox('Kepemilikan Jamban', ('Iya', 'Tidak'))
            ibu_jakes = option = st.selectbox('Jaminan Kesehatan', ('Iya', 'Tidak'))
            
            if st.button("Tambah Data Ibu Hamil"):
                add_data_ibu(ibu_kia,ibu_nama,ibu_status_kehamilan,ibu_perkiraan_tanggal_lahir,
                            ibu_usia_kehamilan,ibu_tanggal_melahirkan,ibu_pemeriksaan,ibu_konsumsi,
                            ibu_nifas,ibu_gizi,ibu_kunjungan,ibu_air_bersih,ibu_jamban,ibu_jakes)
                st.success("Data :'{}' disimpan".format(ibu_nama))
        

    elif choice == "👶 Pemantauan Bulanan Anak":
        st.subheader("👶 Pemantauan Bulanan Anak")
        menu_4 = ["Data Anak", "Data Visualization", "Tambah Data Anak"]
        choice_4 = st.selectbox("Menu", menu_4)
        
        if choice_4 == "Data Anak":
            st.subheader("Data Anak")
            result = view_data_anak()
            clean_db_anak = pd.DataFrame(result, columns = ['No Register','Nama Anak','Jenis Kelamin','Tanggal Lahir',
                                                            'Status Gizi Anak','Umur (Bulan)','Hasil','Pemberian Imunisasi Dasar',
                                                            'Pengukuran Berat Badan','Pengukuran Tinggi Badan',
                                                            'Konseling Gizi Bagi Orang Tua (L)','Konseling Gizi Bagi Orang Tua (P)',
                                                            'Kunjungan Rumah','Kepemilikan Akses Air Bersih','Kepemilikan Jamban Sehat',
                                                            'Akta Lahir','Jaminan Kesehatan','Pengasuhan (PAUD)'])
            AgGrid(clean_db_anak)
            
            st.download_button("Download Data anak", clean_db_anak.to_csv(),file_name = 'data_anak.csv', mime = 'text/csv')
            
            # Delete data
            st.subheader('Hapus Data')
            no_register_anak = [i[0] for i in view_data_anak()]
            delete_data_by_no_register = st.selectbox("Nomor Register", no_register_anak)
            
            if st.button("Hapus Data"):
                delete_data_anak(delete_data_by_no_register)
                st.warning("Data : '{}'".format(delete_data_by_no_register))
                
        if choice_4 == "Data Visualization":
            st.subheader("Data Visualization")
            result = view_data_anak()
            clean_db_anak = pd.DataFrame(result, columns = ['No Register','Nama Anak','Jenis Kelamin','Tanggal Lahir',
                                                            'Status Gizi Anak','Umur (Bulan)','Hasil','Pemberian Imunisasi Dasar',
                                                            'Pengukuran Berat Badan','Pengukuran Tinggi Badan',
                                                            'Konseling Gizi Bagi Orang Tua (L)','Konseling Gizi Bagi Orang Tua (P)',
                                                            'Kunjungan Rumah','Kepemilikan Akses Air Bersih','Kepemilikan Jamban Sehat',
                                                            'Akta Lahir','Jaminan Kesehatan','Pengasuhan (PAUD)'])
        
            plt.style.use('dark_background')
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Jenis Kelamin")
                metrics_anak = clean_db_anak
                ax = sns.countplot(data = metrics_anak, x = 'Jenis Kelamin', orient = 'h')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Status Gizi Anak")
                ax = sns.countplot(data = metrics_anak, x = 'Status Gizi Anak')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                

            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Umur (Bulan)")
                metrics_anak['Umur (Bulan)'].value_counts().plot.pie()
                st.pyplot(transparent=True)
                
            with col2: 
                st.subheader("Tanggal Lahir")
                metrics_anak['Tanggal Lahir'].value_counts().plot(kind='line')
                st.pyplot(transparent=True)
                
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Hasil")
                metrics_anak['Hasil'].value_counts().plot(kind='barh')
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Status Gizi Anak")
                ax = sns.countplot(data = metrics_anak, x = 'Status Gizi Anak')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pengukuran Berat Badan")
                ax = sns.countplot(data = metrics_anak, x = 'Pengukuran Berat Badan')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Pengukuran Tinggi Badan")
                ax = sns.countplot(data = metrics_anak, x = 'Pengukuran Tinggi Badan')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)

            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Konseling Gizi Bagi Orang Tua (L)")
                ax = sns.countplot(data = metrics_anak, x = 'Konseling Gizi Bagi Orang Tua (L)')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Konseling Gizi Bagi Orang Tua (P)")
                ax = sns.countplot(data = metrics_anak, x = 'Konseling Gizi Bagi Orang Tua (P)')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pemberian Imunisasi Dasar")
                ax = sns.countplot(data = metrics_anak, x = 'Pemberian Imunisasi Dasar')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Kunjungan Rumah")
                ax = sns.countplot(data = metrics_anak, x = 'Kunjungan Rumah')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            st.write("")    
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Kepemilikan Akses Air Bersih")
                ax = sns.countplot(data = metrics_anak, x = 'Kepemilikan Akses Air Bersih')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Kepemilikan Jamban Sehat")
                ax = sns.countplot(data = metrics_anak, x = 'Kepemilikan Jamban Sehat')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            st.write("")    
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Akta Lahir")
                ax = sns.countplot(data = metrics_anak, x = 'Akta Lahir')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col2:
                st.subheader("Jaminan Kesehatan")
                ax = sns.countplot(data = metrics_anak, x = 'Jaminan Kesehatan')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
            with col3:
                st.subheader("Pengasuhan (PAUD)")
                ax = sns.countplot(data = metrics_anak, x = 'Pengasuhan (PAUD)')
                for container in ax.containers:
                    ax.bar_label(container)
                st.pyplot(transparent=True)
                
                
        if choice_4 == "Tambah Data Anak":
            st.subheader("Tambah Data Anak")
            create_table_anak()
            
            # Tambah data anak
            anak_kia = st.text_input('Masukkan No Register')
            anak_nama = st.text_input('Masukkan Nama Anak')
            anak_kelamin = option = st.selectbox('Jenis Kelamin', ('L', 'P'))
            anak_tl = st.date_input('Masukkan Tanggal Lahir')
            anak_gizi = option = st.selectbox('Status Gizi Anak (Normal/Buruk/Kurang/Stunting)', ('Normal', 'Buruk', 'Kurang', 'Stunting'))
            anak_umur = st.text_input('Masukkan Umur (Bulan)')
            anak_hasil = option = st.selectbox('Hasil', ('M', 'K', 'H'))
            anak_imun_dasar = option = st.selectbox('Pemberian Imunisasi Dasar', ('Iya', 'Tidak'))
            anak_bb = option = st.selectbox('Pengukuran Berat Badan', ('Iya', 'Tidak'))
            anak_tb = option = st.selectbox('Pengukuran Tinggi Badan', ('Iya', 'Tidak'))
            anak_konseling_l = option = st.selectbox('Konseling Gizi Bagi Orang Tua (L)', ('Iya', 'Tidak'))
            anak_konseling_p = option = st.selectbox('Konseling Gizi Bagi Orang Tua (P)', ('Iya', 'Tidak'))
            anak_kunjungan = option = st.selectbox('Kunjungan Rumah', ('Iya', 'Tidak'))
            anak_air = option = st.selectbox('Kepemilikan Akses Air Bersih', ('Iya', 'Tidak'))
            anak_jamban = option = st.selectbox('Kepemilikan Jamban Sehat', ('Iya', 'Tidak'))
            anak_akta = option = st.selectbox('Akta Lahir', ('Iya', 'Tidak'))
            anak_jakes = option = st.selectbox('Jaminan Kesehatan', ('Iya', 'Tidak'))
            anak_paud = option = st.selectbox('Pengasuhan (PAUD)', ('Iya', 'Tidak'))
            
            
            if st.button("Tambah Data Anak"):
                add_data_anak(anak_kia,anak_nama,anak_kelamin,anak_tl,anak_gizi,anak_umur,anak_hasil,anak_imun_dasar,anak_bb,anak_tb,anak_konseling_l,anak_konseling_p,anak_kunjungan,anak_air,anak_jamban,anak_akta,anak_jakes,anak_paud)
                st.success("Data :'{}' disimpan".format(anak_nama))
        
        
        
if __name__ == '__main__':
    main()