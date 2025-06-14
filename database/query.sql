-- Drop tables in reverse order of dependency
DROP TABLE IF EXISTS otp CASCADE;
DROP TABLE IF EXISTS notifikasi CASCADE;
DROP TABLE IF EXISTS penyewaan CASCADE;
DROP TABLE IF EXISTS kelengkapan CASCADE;
DROP TABLE IF EXISTS list_jadwal CASCADE;
DROP TABLE IF EXISTS produk CASCADE;
DROP TABLE IF EXISTS toko CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS admin CASCADE;


-- Tabel Admin
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR,
    pass VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    no_telp VARCHAR
);

-- Tabel User
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR,
    pass VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    no_telp VARCHAR,
    alamat TEXT,
    latitude FLOAT,
    longitude FLOAT,
    ktp VARCHAR,
    point INT,
    selfie VARCHAR,
    status VARCHAR CHECK (status IN ('active', 'inactive'))
);

-- Tabel Toko
CREATE TABLE toko (
    id SERIAL PRIMARY KEY,
    nama_toko VARCHAR,
    keterangan TEXT,
    latitude FLOAT,
    longitude FLOAT,
    id_admin INT,
    waktu_buka TIME,
    waktu_tutup TIME,
    CONSTRAINT fk_toko_admin FOREIGN KEY (id_admin) REFERENCES admin(id)
);

-- Tabel Produk
CREATE TABLE produk (
    id SERIAL PRIMARY KEY,
    nama_produk VARCHAR,
    warna VARCHAR,
    harga_sewa INT,
    idtoko INT,
    jadwal JSON,
    status_sewa BOOLEAN,
    keterangan TEXT,
    img VARCHAR,
    status VARCHAR CHECK (status IN ('active', 'inactive')),
    CONSTRAINT fk_produk_toko FOREIGN KEY (idtoko) REFERENCES toko(id)
);

-- Tabel List Jadwal
CREATE TABLE list_jadwal (
    id SERIAL PRIMARY KEY,
    produk_id INT,
    jadwal_mulai DATE,
    jadwal_berakhir DATE,
    CONSTRAINT fk_list_jadwal_produk FOREIGN KEY (produk_id) REFERENCES produk(id)
);

-- Tabel Kelengkapan
CREATE TABLE kelengkapan (
    id SERIAL PRIMARY KEY,
    produk_id INT,
    charger BOOLEAN,
    case BOOLEAN,
    CONSTRAINT fk_kelengkapan_produk FOREIGN KEY (produk_id) REFERENCES produk(id)
);

-- Tabel Penyewaan
CREATE TABLE penyewaan (
    id SERIAL PRIMARY KEY,
    produk_id INT,
    user_id INT,
    admin_id INT,
    komentar TEXT,
    tanggal_mulai DATE,
    tanggal_selesai DATE,
    status VARCHAR CHECK (status IN ('selesai', 'ditolak', 'pending', 'cancel')),
    CONSTRAINT fk_penyewaan_produk FOREIGN KEY (produk_id) REFERENCES produk(id),
    CONSTRAINT fk_penyewaan_user FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT fk_penyewaan_admin FOREIGN KEY (admin_id) REFERENCES admin(id)
);

-- Tabel Notifikasi
CREATE TABLE notifikasi (
    id SERIAL PRIMARY KEY,
    notifikasi TEXT,
    user_id INT,
    admin_id INT,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES "user"(id),
    CONSTRAINT fk_notif_admin FOREIGN KEY (admin_id) REFERENCES admin(id)
);

-- Tabel OTP
CREATE TABLE otp (
    id SERIAL PRIMARY KEY,
    user_id INT,
    otp VARCHAR,
    CONSTRAINT fk_otp_user FOREIGN KEY (user_id) REFERENCES "user"(id)
);


-- Admin
INSERT INTO admin (username, pass, nama, email, no_telp)
VALUES 
('admin1', 'pass123', 'Admin Satu', 'admin1@mail.com', '081234567890'),
('admin2', 'pass456', 'Admin Dua', 'admin2@mail.com', '081234567891');

-- User
INSERT INTO "user" (username, pass, nama, email, no_telp, alamat, latitude, longitude, ktp, point, selfie, status)
VALUES 
('user1', 'pass1', 'User Satu', 'user1@mail.com', '0821111111', 'Jl Mawar No.1', -7.6, 110.2, '1234567890123456', 100, 'selfie1.jpg', 'active'),
('user2', 'pass2', 'User Dua', 'user2@mail.com', '0822222222', 'Jl Melati No.2', -7.7, 110.3, '2345678901234567', 200, 'selfie2.jpg', 'inactive');

-- Toko
INSERT INTO toko (nama_toko, keterangan, latitude, longitude, id_admin, waktu_buka, waktu_tutup)
VALUES 
('Toko A', 'Menyediakan alat outdoor', -7.6, 110.3, 1, '08:00', '17:00'),
('Toko B', 'Pusat persewaan elektronik', -7.7, 110.4, 2, '09:00', '18:00');

-- Produk
INSERT INTO produk (nama_produk, warna, harga_sewa, idtoko, jadwal, status_sewa, keterangan, img, status)
VALUES 
('Kamera DSLR', 'Hitam', 150000, 1, '{"jadwal": []}', false, 'Kamera profesional', 'kamera.jpg', 'active'),
('Proyektor Mini', 'Putih', 100000, 2, '{"jadwal": []}', true, 'Cocok untuk presentasi', 'proyektor.jpg', 'inactive');

-- List Jadwal
INSERT INTO list_jadwal (produk_id, jadwal_mulai, jadwal_berakhir)
VALUES 
(1, '2025-06-20', '2025-06-22'),
(2, '2025-06-18', '2025-06-19');

-- Kelengkapan
INSERT INTO kelengkapan (produk_id, charger, case)
VALUES 
(1, true, true),
(2, false, true);

-- Penyewaan
INSERT INTO penyewaan (produk_id, user_id, admin_id, komentar, tanggal_mulai, tanggal_selesai, status)
VALUES 
(1, 1, 1, 'Penyewaan cepat & mudah', '2025-06-10', '2025-06-12', 'selesai'),
(2, 2, 2, 'Alat bagus tapi agak berat', '2025-06-08', '2025-06-10', 'selesai');

-- Notifikasi
INSERT INTO notifikasi (notifikasi, user_id, admin_id)
VALUES 
('Pesanan Anda telah dikonfirmasi', 1, 1),
('Penyewaan Anda sudah selesai', 2, 2);

-- OTP
INSERT INTO otp (user_id, otp)
VALUES 
(1, '123456'),
(2, '654321');
