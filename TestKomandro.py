import mysql.connector  

# Function to create a database connection
def connection(database=None):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database
    )

# Function to create a database and its tables
def membuat_database_dan_tabel(cursor): 
    cursor.execute("CREATE DATABASE IF NOT EXISTS BARANG")
    print("Database BARANG berhasil dibuat")
    
    cursor.execute("USE BARANG") 
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS barang (
            id_barang INT AUTO_INCREMENT PRIMARY KEY,
            nama_barang VARCHAR(100) NOT NULL,
            kategori_barang VARCHAR(50),
            harga DECIMAL(10, 2) NOT NULL,
            stok INT NOT NULL,
            deskripsi TEXT,
            tanggal_masuk DATE NOT NULL
        )
    """)
    print("Tabel barang berhasil dibuat")

# Class to represent an item in inventory
class Barang:
    def __init__(self, id_barang, nama_barang, kategori_barang, harga, stok, deskripsi, tanggal_masuk):
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.kategori_barang = kategori_barang
        self.harga = harga
        self.stok = stok
        self.deskripsi = deskripsi
        self.tanggal_masuk = tanggal_masuk

# Class to manage inventory operations
class Inventory:
    def __init__(self):
        self.db = connection("BARANG")
        self.cursor = self.db.cursor()  # Create a cursor for executing queries

    def close_connection(self):
        # Close the database cursor and connection
        self.cursor.close()
        self.db.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)  
            else:
                self.cursor.execute(query)  
            self.db.commit()  
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}") 

    def lihat_barang(self):
        try:
            self.cursor.execute("SELECT * FROM barang")  
            result = self.cursor.fetchall()  
            if not result:
                print("Tidak ada barang di inventaris.")  
            else:
                print("Daftar Barang:")
                for barang in result:
                    print(f"ID: {barang[0]}, Nama: {barang[1]}, Stok: {barang[4]}, Harga: {barang[3]}, Kategori: {barang[2]}, Deskripsi: {barang[5]}, Tanggal Masuk: {barang[6]}")
            # Menulis data barang ke file teks
            with open("data_barang.txt", "w") as file:  # Overwrite existing data in file
                for barang in result:
                    file.write(f"ID: {barang[0]}, Nama: {barang[1]}, Stok: {barang[4]}, Harga: {barang[3]}, Kategori: {barang[2]}, Deskripsi: {barang[5]}, Tanggal Masuk: {barang[6]}\n")
            print("Data barang berhasil ditulis ke file teks.")
        except mysql.connector.Error as err:
            print(f"Error retrieving barang: {err}") 

    def tambah_barang(self, barang):
        self.execute_query(
            "INSERT INTO barang (nama_barang, kategori_barang, harga, stok, deskripsi, tanggal_masuk) VALUES (%s, %s, %s, %s, %s, %s)",
            (barang.nama_barang, barang.kategori_barang, barang.harga, barang.stok, barang.deskripsi, barang.tanggal_masuk)
        )
        print(f"Barang '{barang.nama_barang}' berhasil ditambahkan.") 
        self.lihat_barang()  # Update file txt after adding

    def update_stok_barang(self, id_barang, stok_baru):
        self.execute_query("UPDATE barang SET stok = %s WHERE id_barang = %s", (stok_baru, id_barang))
        print(f"Stok barang dengan ID {id_barang} berhasil diperbarui menjadi {stok_baru}.")
        self.lihat_barang()  # Update file txt after updating

    def hapus_barang(self, id_barang):
        self.execute_query("DELETE FROM barang WHERE id_barang = %s", (id_barang,))
        print(f"Barang dengan ID {id_barang} berhasil dihapus.")  
        self.lihat_barang()  # Update file txt after deleting

# Example usage
if __name__ == "__main__":
    db = connection()  # Create initial connection to the database
    cursor = db.cursor()  # Create a cursor for executing queries

    try:
        membuat_database_dan_tabel(cursor)  # Create database and tables
    except mysql.connector.Error as err:
        print(f"Error during database setup: {err}") 
    finally:
        cursor.close()  
        db.close()      

    inventory = Inventory()
    
    # Create new Barang objects
    barang1 = Barang(None, "Laptop", "Elektronik", 15000000, 10, "Laptop Gaming", "2024-09-01")
    barang2 = Barang(None, "Mouse", "Aksesoris", 150000, 50, "Mouse Wireless", "2024-09-10")

    inventory.tambah_barang(barang1)  # Add first item to inventory
    inventory.tambah_barang(barang2)  # Add second item to inventory
    inventory.lihat_barang()  # Display all items in the inventory
    inventory.update_stok_barang(1, 8)  # Update stock for the first item
    inventory.lihat_barang()  # Display all items again after stock update
    inventory.hapus_barang(2)  # Delete the second item
    inventory.lihat_barang()  # Display all items again after deletion
    inventory.close_connection()  # Close inventory connection
