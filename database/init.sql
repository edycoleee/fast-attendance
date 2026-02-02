-- ============================================================
-- INITIALIZATION SQL FOR RSUD SULFAT ATTENDANCE SYSTEM
-- ============================================================
-- Converted from MySQL to PostgreSQL
-- Database: attendance_db
-- ============================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- TABLE: lokasi
-- ============================================================
CREATE TABLE IF NOT EXISTS lokasi (
    id_lokasi SERIAL PRIMARY KEY,
    nama_lokasi VARCHAR(255),
    lat VARCHAR(255),
    long VARCHAR(255),
    jarak_area INTEGER
);

-- ============================================================
-- TABLE: ruang
-- ============================================================
CREATE TABLE IF NOT EXISTS ruang (
    id_ruang SERIAL PRIMARY KEY,
    nama_ruang VARCHAR(255),
    status VARCHAR(15)
);

-- ============================================================
-- TABLE: pegawai
-- ============================================================
CREATE TABLE IF NOT EXISTS pegawai (
    id_pegawai VARCHAR(20) PRIMARY KEY,
    nip VARCHAR(255),
    nama VARCHAR(255),
    jenis_kelamin VARCHAR(255),
    tempat_lahir VARCHAR(255),
    tanggal_lahir DATE,
    alamat TEXT,
    id_ruang INTEGER,
    status VARCHAR(15),
    create_at VARCHAR(255),
    create_date TIMESTAMP,
    foto VARCHAR(100),
    FOREIGN KEY (id_ruang) REFERENCES ruang(id_ruang)
);

-- ============================================================
-- TABLE: absensi
-- ============================================================
CREATE TABLE IF NOT EXISTS absensi (
    id_absensi VARCHAR(11) PRIMARY KEY,
    id_lokasi INTEGER,
    id_pegawai VARCHAR(20) DEFAULT '',
    uid VARCHAR(30),
    tanggal TIMESTAMP,
    ket VARCHAR(50),
    ipaddress VARCHAR(20),
    FOREIGN KEY (id_lokasi) REFERENCES lokasi(id_lokasi),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- ============================================================
-- TABLE: shift
-- ============================================================
CREATE TABLE IF NOT EXISTS shift (
    id_shift SERIAL PRIMARY KEY,
    nama_shift VARCHAR(255),
    jam_masuk VARCHAR(255),
    jam_keluar VARCHAR(255)
);

-- ============================================================
-- TABLE: shift_pegawai
-- ============================================================
CREATE TABLE IF NOT EXISTS shift_pegawai (
    id_shift_pegawai VARCHAR(20) PRIMARY KEY,
    tahun VARCHAR(255),
    bulan VARCHAR(255),
    id_ruang INTEGER,
    create_at VARCHAR(255),
    create_date TIMESTAMP,
    FOREIGN KEY (id_ruang) REFERENCES ruang(id_ruang)
);

-- ============================================================
-- TABLE: detail_shift_pegawai
-- ============================================================
CREATE TABLE IF NOT EXISTS detail_shift_pegawai (
    id_detail_shift_pegawai VARCHAR(20) PRIMARY KEY,
    id_shift_pegawai VARCHAR(20),
    id_pegawai VARCHAR(20),
    hari01 VARCHAR(20),
    hari02 VARCHAR(20),
    hari03 VARCHAR(20),
    hari04 VARCHAR(20),
    hari05 VARCHAR(20),
    hari06 VARCHAR(20),
    hari07 VARCHAR(20),
    hari08 VARCHAR(20),
    hari09 VARCHAR(20),
    hari10 VARCHAR(20),
    hari11 VARCHAR(20),
    hari12 VARCHAR(20),
    hari13 VARCHAR(20),
    hari14 VARCHAR(20),
    hari15 VARCHAR(20),
    hari16 VARCHAR(20),
    hari17 VARCHAR(20),
    hari18 VARCHAR(20),
    hari19 VARCHAR(20),
    hari20 VARCHAR(20),
    hari21 VARCHAR(20),
    hari22 VARCHAR(20),
    hari23 VARCHAR(20),
    hari24 VARCHAR(20),
    hari25 VARCHAR(20),
    hari26 VARCHAR(20),
    hari27 VARCHAR(20),
    hari28 VARCHAR(20),
    hari29 VARCHAR(20),
    hari30 VARCHAR(20),
    hari31 VARCHAR(20),
    FOREIGN KEY (id_shift_pegawai) REFERENCES shift_pegawai(id_shift_pegawai),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- ============================================================
-- TABLE: keterangan_absen
-- ============================================================
CREATE TABLE IF NOT EXISTS keterangan_absen (
    id_pegawai VARCHAR(20) NOT NULL,
    tanggal DATE,
    keterangan VARCHAR(255),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- ============================================================
-- TABLE: login_absensi
-- ============================================================
CREATE TABLE IF NOT EXISTS login_absensi (
    id_login_absensi SERIAL PRIMARY KEY,
    id_pegawai VARCHAR(20) DEFAULT '',
    uid VARCHAR(50),
    player_id VARCHAR(50),
    model VARCHAR(250),
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai)
);

-- ============================================================
-- TABLE: pesan
-- ============================================================
CREATE TABLE IF NOT EXISTS pesan (
    id_pesan SERIAL PRIMARY KEY,
    kepada VARCHAR(50),
    id_ruang VARCHAR(255),
    id_pegawai VARCHAR(255),
    judul VARCHAR(255),
    isi_pesan TEXT,
    create_at VARCHAR(200),
    create_date TIMESTAMP
);

-- ============================================================
-- TABLE: pesan_detail
-- ============================================================
CREATE TABLE IF NOT EXISTS pesan_detail (
    id_detail_pesan BIGSERIAL PRIMARY KEY,
    id_pesan INTEGER NOT NULL,
    id_pegawai VARCHAR(50),
    status_baca VARCHAR(50),
    update_date TIMESTAMP,
    FOREIGN KEY (id_pesan) REFERENCES pesan(id_pesan)
);

-- ============================================================
-- TABLE: userlevels
-- ============================================================
CREATE TABLE IF NOT EXISTS userlevels (
    userlevelid INTEGER PRIMARY KEY,
    userlevelname VARCHAR(255) NOT NULL
);

-- ============================================================
-- TABLE: userlevelpermissions
-- ============================================================
CREATE TABLE IF NOT EXISTS userlevelpermissions (
    userlevelid INTEGER NOT NULL,
    tablename VARCHAR(255) NOT NULL,
    permission INTEGER NOT NULL,
    PRIMARY KEY (userlevelid, tablename),
    FOREIGN KEY (userlevelid) REFERENCES userlevels(userlevelid)
);

-- ============================================================
-- TABLE: user
-- ============================================================
CREATE TABLE IF NOT EXISTS "user" (
    id_user SERIAL PRIMARY KEY,
    id_pegawai VARCHAR(15),
    username VARCHAR(255),
    password VARCHAR(255),
    level_id INTEGER,
    status INTEGER,
    FOREIGN KEY (id_pegawai) REFERENCES pegawai(id_pegawai),
    FOREIGN KEY (level_id) REFERENCES userlevels(userlevelid)
);

-- ============================================================
-- CREATE INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_absensi_id_lokasi ON absensi(id_lokasi);
CREATE INDEX IF NOT EXISTS idx_absensi_id_pegawai ON absensi(id_pegawai);
CREATE INDEX IF NOT EXISTS idx_detail_shift_pegawai_id_pegawai ON detail_shift_pegawai(id_pegawai);
CREATE INDEX IF NOT EXISTS idx_detail_shift_pegawai_id_shift_pegawai ON detail_shift_pegawai(id_shift_pegawai);
CREATE INDEX IF NOT EXISTS idx_shift_pegawai_id_ruang ON shift_pegawai(id_ruang);
CREATE INDEX IF NOT EXISTS idx_user_id_pegawai ON "user"(id_pegawai);
CREATE INDEX IF NOT EXISTS idx_user_level_id ON "user"(level_id);
CREATE INDEX IF NOT EXISTS idx_pegawai_id_ruang ON pegawai(id_ruang);

-- ============================================================
-- VIEW: v_shift
-- ============================================================
CREATE OR REPLACE VIEW v_shift AS
SELECT 
    id_shift,
    nama_shift,
    CONCAT('(', jam_masuk, '-', jam_keluar, ')') AS ket_shift
FROM shift;

-- ============================================================
-- VIEW: v_shiftpeg
-- ============================================================
CREATE OR REPLACE VIEW v_shiftpeg AS
SELECT id_shift_pegawai, id_pegawai, '01' AS hari, hari01 AS shift FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '02', hari02 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '03', hari03 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '04', hari04 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '05', hari05 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '06', hari06 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '07', hari07 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '08', hari08 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '09', hari09 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '10', hari10 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '11', hari11 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '12', hari12 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '13', hari13 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '14', hari14 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '15', hari15 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '16', hari16 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '17', hari17 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '18', hari18 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '19', hari19 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '20', hari20 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '21', hari21 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '22', hari22 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '23', hari23 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '24', hari24 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '25', hari25 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '26', hari26 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '27', hari27 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '28', hari28 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '29', hari29 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '30', hari30 FROM detail_shift_pegawai
UNION ALL SELECT id_shift_pegawai, id_pegawai, '31', hari31 FROM detail_shift_pegawai;

-- ============================================================
-- VIEW: v_user_pegawai
-- ============================================================
CREATE OR REPLACE VIEW v_user_pegawai AS
SELECT 
    p.id_pegawai,
    p.nama,
    p.nip,
    u.username
FROM "user" u
LEFT JOIN pegawai p ON u.id_pegawai = p.id_pegawai;

-- ============================================================
-- INSERT SAMPLE DATA
-- ============================================================

-- Sample ruang
INSERT INTO ruang (id_ruang, nama_ruang, status) 
VALUES (1, 'IT Department', 'aktif')
ON CONFLICT (id_ruang) DO NOTHING;

-- Sample shift
INSERT INTO shift (id_shift, nama_shift, jam_masuk, jam_keluar) 
VALUES (1, 'Pagi', '08:00', '16:00')
ON CONFLICT (id_shift) DO NOTHING;

-- Sample lokasi
INSERT INTO lokasi (id_lokasi, nama_lokasi, lat, long, jarak_area) 
VALUES (1, 'RSUD Sulfat', '-6.200000', '106.816666', 100)
ON CONFLICT (id_lokasi) DO NOTHING;

-- Sample userlevel
INSERT INTO userlevels (userlevelid, userlevelname) 
VALUES (1, 'Administrator'), (2, 'User'), (3, 'Guest')
ON CONFLICT (userlevelid) DO NOTHING;

-- ============================================================
-- GRANT PERMISSIONS
-- ============================================================
GRANT ALL PRIVILEGES ON DATABASE attendance_db TO sultan;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sultan;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sultan;

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'RSUD Sulfat Attendance Database initialization completed!';
    RAISE NOTICE 'Total Tables: 17';
    RAISE NOTICE 'Total Views: 3';
    RAISE NOTICE '============================================================';
END $$;
