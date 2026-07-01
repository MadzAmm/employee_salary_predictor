
-- =============================================================================================
-- DATA QUALITY CHECK (EDA)
-- Catatan: Pengecekan awal pada dataset mengonfirmasi bahwa data sudah bersih. Tidak ditemukan 
-- missing values (NULL), tidak ada data duplikat, dan semua tipe data sudah sesuai untuk analisis.
-- =============================================================================================

-- 1. Data type checking

TABLE employee_salary;

DESC employee_salary

-- Jika hendak merubah tipe data maka bisa lakukan alter table modify 

ALTER TABLE employee_salary MODIFY COLUMN employee_id VARCHAR(20);
ALTER TABLE employee_salary MODIFY COLUMN employee_id TEXT;

-- 2. Duplikat data checking

WITH duplicate_data AS(
    SELECT * , ROW_NUMBER() OVER(PARTITION BY employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, annual_salary_usd ORDER BY employee_id) AS row_num
FROM employee_salary
)
SELECT *
FROM duplicate_data
WHERE row_num > 1
;

-- i: 0 data duplikat

-- jika ada data duplikat maka bisa lakukan DELETE dengan menggunakan temporary table karena cte di mysql tidak bisa diupdate. berikut trik delete duplikat data di mysql.

-- a. cek data duplikat menggunakan row_number()
WITH duplicate_data AS(
    SELECT * , ROW_NUMBER() OVER(PARTITION BY employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, remote_work, annual_salary_usd ORDER BY employee_id) AS row_num
FROM employee_salary
)
SELECT * FROM duplicate_data WHERE row_num > 1;

-- b. buat temporary table yang disamakan kolomnya seperti tabel employee salary
CREATE TEMPORARY TABLE temp_duplicate_data LIKE employee_salary;

-- c. karena di kueri pengecekan ada penambahan kolom baru yaitu row_num maka tambahkan juga pada temporary table agar ketika di insert kolomnya matching.
ALTER TABLE temp_duplicate_data ADD COLUMN row_num INT;

-- d. insert data lengkap ke temporary table
INSERT INTO temp_duplicate_data
SELECT * , ROW_NUMBER() OVER(PARTITION BY employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, remote_work, annual_salary_usd ORDER BY employee_id) AS row_num
FROM employee_salary;

-- INFO PENTING proses abcd bisa disingkat dengan insert data langsung ketika membuat temporary table
CREATE TEMPORARY TABLE temp_duplicate_data AS
SELECT * , ROW_NUMBER() OVER(PARTITION BY employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, remote_work, annual_salary_usd ORDER BY employee_id) AS row_num
FROM employee_salary;

DROP TABLE temp_duplicate_data;


-- e. delete duplikat di temporary table
DELETE 
FROM temp_duplicate_data
WHERE row_num > 1;

-- f. cek untuk memastikan
SELECT * 
FROM temp_duplicate_data
WHERE row_num > 1;

-- g. Hapus kolom row_num dari tabel temporary agar strukturnya kembali sama dengan tabel asli agar match sehingga bisa menjadi value yang nantinya diinsert ke tabel asli.
ALTER TABLE temp_duplicate_data DROP COLUMN row_num;

-- h. Kosongkan tabel asli
TRUNCATE TABLE employee_salary;

TABLE employee_salary;

-- i. insert data tabel asli dari temporary table yang duplikat datanya sudah dihapus.
INSERT INTO employee_salary
SELECT * FROM temp_duplicate_data;

-- HAPUS DUPLIKAT DATA SELESAI ============

-- 2. Missing Value Checking & Handling

SELECT 
    SUM(CASE WHEN employee_id IS NULL THEN 1 ELSE 0 END) employee_id_null,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) age_null,
    SUM(CASE WHEN years_experience IS NULL THEN 1 ELSE 0 END) years_experience_null,
    SUM(CASE WHEN education_level IS NULL THEN 1 ELSE 0 END) educaion_level_null,
    SUM(CASE WHEN job_role IS NULL THEN 1 ELSE 0 END) job_role_null,
    SUM(CASE WHEN city_tier IS NULL THEN 1 ELSE 0 END) city_tier_null,
    SUM(CASE WHEN performance_score IS NULL THEN 1 ELSE 0 END) performance_score_null,
    SUM(CASE WHEN num_skills IS NULL THEN 1 ELSE 0 END) nnum_skills_null,
    SUM(CASE WHEN annual_salary_usd IS NULL THEN 1 ELSE 0 END) annual_salary_usd_null
FROM employee_salary;
    

-- i: data missing = 0

-- =============================================================================================
-- CARA MENGHANDLE MISSING VALUE JIKA ADA
-- ada 2 pendekatan utama untuk menanganinya:

-- OPSI 1: Menghapus baris yang memiliki missing value (DELETE)
-- Biasanya dilakukan jika data yang hilang ada di kolom kritikal (misal: employee_id atau job_role).

-- Jika ingin menghapus baris HANYA JIKA SEMUA kolom bernilai NULL (baris benar-benar kosong) mirip AND:
DELETE FROM employee_salary
WHERE COALESCE(employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, remote_work, annual_salary_usd) IS NULL;

-- Jika ingin menghapus baris Minimal ada satu kolom yang bernilai NULL
DELETE FROM employee_salary
WHERE employee_id IS NULL OR job_role IS NULL OR age IS NULL OR years_experience IS NULL OR education_level IS NULL OR city_tier IS NULL OR performance_score IS NULL OR num_skills IS NULL OR annual_salary_usd IS NULL;

-- atau dengan trik CONCAT (mirip mekanisme or)
DELETE FROM employee_salary
WHERE CONCAT(employee_id, job_role, age, years_experience, education_level, city_tier, performance_score, num_skills, remote_work, annual_salary_usd) IS NULL;

-- OPSI 2: Mengisi missing value (Imputation)
-- Biasanya dilakukan menggunakan nilai default, rata-rata (mean), atau nilai tertentu.

-- Contoh mengisi NULL pada years_experience dengan angka 0
UPDATE employee_salary SET years_experience = 0 WHERE years_experience IS NULL;

-- Contoh mengisi NULL pada education_level dengan label 'Unknown'
UPDATE employee_salary SET education_level = 'Unknown' WHERE education_level IS NULL;



-- =============================================================================================

-- 1. Get the total salary, average salary, maximum salary, minimum salary, standar deviation of salary, salary range, total number of employees, and total number of unique employees from the employee_salary table.

SELECT SUM(annual_salary_usd) total_salary, 
    AVG(annual_salary_usd) average_salary,
    MAX(annual_salary_usd) max_salary,
    MIN(annual_salary_usd) min_salary,
    STDDEV(annual_salary_usd) salary_standard_deviation,
    MAX(annual_salary_usd) - MIN(annual_salary_usd) salary_range,
    COUNT(employee_id) total_employees,
    COUNT(DISTINCT employee_id) unique_employees
FROM employee_salary
;



-- =============================================================================================

-- 2. Get the total salary, average salary, maximum salary, minimum salary, total number of employees, and total number of unique employees for each job role from the employee_salary table.

SELECT job_role, 
    SUM(annual_salary_usd) total_salary, 
    AVG(annual_salary_usd) average_salary,
    MAX(annual_salary_usd) max_salary,
    MIN(annual_salary_usd) min_salary,
    STDDEV(annual_salary_usd) salary_standard_deviation,
    MAX(annual_salary_usd) - MIN(annual_salary_usd) salary_range,
    COUNT(employee_id) total_employees,
    COUNT(DISTINCT employee_id) unique_employees
FROM employee_salary
GROUP BY job_role
;

-- =============================================================================================

-- 3. Get the MIN and MAX salary for each job role from the employee_salary table.

SELECT job_role,
    MIN(annual_salary_usd) min_salary,
    MAX(annual_salary_usd) max_salary
FROM employee_salary
GROUP BY job_role
ORDER BY MAX(annual_salary_usd) DESC
;

-- =============================================================================================

-- 4. Is education level associated with higher salaries? Get the average salary for each education level from the employee_salary table.

SELECT education_level, 
    AVG(annual_salary_usd) average_salary,
    DENSE_RANK() OVER (ORDER BY AVG(annual_salary_usd) DESC) salary_rank
FROM employee_salary
GROUP BY education_level
ORDER BY average_salary DESC
;

-- i: semakin tinggi education level, semakin tinggi pula average salary.

-- =============================================================================================

-- 5. Is there a relationship between years of experience and salary? Get the average salary for each range of years of experience from the employee_salary table.

SELECT DISTINCT years_experience
FROM employee_salary
ORDER BY years_experience;

SELECT 
    CASE
        WHEN years_experience BETWEEN 0 AND 10 THEN 'Intern'
        WHEN years_experience BETWEEN 11 AND 20 THEN 'Junior'
        WHEN years_experience BETWEEN 21 AND 30 THEN 'Mid-level'
        WHEN years_experience BETWEEN 31 AND 40 THEN 'Senior'
        ELSE 'Veteran'
    END AS experience_range,
    AVG(annual_salary_usd) average_salary,
    DENSE_RANK() OVER (ORDER BY AVG(annual_salary_usd) DESC) salary_rank
FROM employee_salary
GROUP BY experience_range;

-- i: semakin tinggi years of experience, semakin tinggi pula average salary.

-- =============================================================================================

-- 6. Which job roles have the highest average salaries? Get the average salary for each job role and rank them from highest to lowest from the employee_salary table.

SELECT job_role, 
    AVG(annual_salary_usd) average_salary,
    DENSE_RANK() OVER (ORDER BY AVG(annual_salary_usd) DESC) salary_rank,
    COUNT(employee_id) total_employees
FROM employee_salary
GROUP BY job_role
;

-- i: Job role yang memiliki avg salary tertinggi adalah DevOps, diikuti oleh ML Engineer, QA Engineer, dan job role yang memiliki avg salary terendah adalah Product Manager. 

-- =============================================================================================

-- 7. Is num_skills associated with higher salaries? Get the average salary for each range of num_skills from the employee_salary table.

SELECT DISTINCT num_skills
FROM employee_salary
ORDER BY num_skills;

SELECT 
    CASE
        WHEN num_skills BETWEEN 0 AND 5 THEN 'Intermediate skills'
        WHEN num_skills BETWEEN 6 AND 10 THEN 'Advanced skills'
        ELSE 'Expert skills'
    END AS skill_range,
    AVG(annual_salary_usd) average_salary,
    DENSE_RANK() OVER (ORDER BY AVG(annual_salary_usd) DESC) salary_rank
FROM employee_salary
GROUP BY skill_range;

-- i: semakin tinggi num_skills, semakin tinggi pula average salary.

-- =============================================================================================

-- 8. How many employees have good performance scores but their salaries are under the average of each job role? Get the average salary for each job role and compare it with the performance_score of each employee from the employee_salary table and then count such employees by job role.

-- option 1: use with cte and join 

WITH avg_salary_by_job_role AS (
    SELECT job_role, AVG(annual_salary_usd) average_salary
    FROM employee_salary
    GROUP BY job_role
) 
SELECT e.job_role, COUNT(e.employee_id) underpaid_employees
FROM employee_salary e  
JOIN avg_salary_by_job_role a ON e.job_role = a.job_role
WHERE e.performance_score > 4 AND e.annual_salary_usd < a.average_salary
GROUP BY e.job_role
ORDER BY underpaid_employees DESC
;

-- option 2: use subquery
SELECT job_role, COUNT(employee_id) underpaid_employees
FROM employee_salary
WHERE performance_score > 4 AND annual_salary_usd < (
    SELECT AVG(annual_salary_usd) 
    FROM employee_salary 
    WHERE job_role = employee_salary.job_role
)GROUP BY job_role
ORDER BY underpaid_employees DESC;

-- option 3: use with cte and window function
WITH salary_rank AS (
    SELECT job_role, employee_id, performance_score, annual_salary_usd, num_skills,
        years_experience,
        AVG(annual_salary_usd) OVER (PARTITION BY job_role) average_salary,
        COUNT(employee_id) OVER (PARTITION BY job_role) total_employees
    FROM employee_salary
)
SELECT job_role, COUNT(employee_id) underpaid_employees, total_employees, COUNT(employee_id) / total_employees percentage_underpaid_employees, AVG(num_skills) avg_num_skills, AVG(years_experience) avg_years_experience
FROM salary_rank
WHERE performance_score > 4 AND annual_salary_usd < average_salary
GROUP BY job_role, total_employees
ORDER BY underpaid_employees DESC -- ORDER BY percentage_underpaid_employees DESC;

-- i: Job role yang memiliki jumlah karyawan dengan performance score diatas 4 tetapi gaji di bawah rata-rata masing-masing job role terbanyak adalah DevOps, diikuti oleh Data Analyst, dan QA Engineer. Namun, jika dilihat dari persentase karyawan yang underpaid dibandingkan dengan total karyawan di masing-masing job role, maka job role yang memiliki persentase karyawan underpaid terbanyak secara berurutan adalah DevOps, ML Engineer, dan Software Engineer. 

-- =============================================================================================

-- 9. How many employees are "overpaid" but have poor performance? Get employees with performance_score < 4 but their salaries are above the average of their job role.

WITH salary_rank AS (
    SELECT job_role, employee_id, performance_score, annual_salary_usd,
        AVG(annual_salary_usd) OVER (PARTITION BY job_role) average_salary,
        COUNT(employee_id) OVER (PARTITION BY job_role) total_employees,
        num_skills,
        years_experience
        
    FROM employee_salary
)
SELECT job_role, COUNT(employee_id) overpaid_employees, total_employees, COUNT(employee_id) / total_employees percentage_overpaid_employees, AVG(num_skills) avg_num_skills, AVG(years_experience) vg_years_experience
FROM salary_rank
WHERE performance_score < 4 AND annual_salary_usd > average_salary
GROUP BY job_role, total_employees
ORDER BY overpaid_employees DESC

-- =============================================================================================

-- 10. Which job roles have the highest salary disparity (variance)? Use Standard Deviation to measure the salary spread within each role.


SELECT job_role,
    COUNT(employee_id) total_employees,
    ROUND(AVG(annual_salary_usd), 2) average_salary,
    ROUND(STDDEV(annual_salary_usd), 2) salary_standard_deviation,
    MAX(annual_salary_usd) - MIN(annual_salary_usd) salary_range
FROM employee_salary
GROUP BY job_role
ORDER BY salary_standard_deviation DESC;

-- i: QA Engineer memiliki std dev tertinggi yang artinya ada ketimpangan gaji yang cukup tinggi antar satu karyawan dengan karyawan lainnya (belum mempertimbangkan variabel atau feature lain) meskipun salary rangenya lebih kecil dari Data Analyst.catatan; std dev berbicara mengenai perhitungan mayoritas titik data seberapa jauh rata-rata gaji karywan menyimpang dari rata-rata dari gaji bukan nilai ekstrem yang mana itu dilakukan oleh perhitungan dua titik max-min.

-- =============================================================================================

-- 11. Side-by-side comparison: Overpaid (Low Performers) vs Underpaid (High Performers). Do Overpaid employees actually have less experience and skills?

WITH employee_status AS (
    SELECT job_role, employee_id, performance_score, annual_salary_usd, num_skills, years_experience,
        AVG(annual_salary_usd) OVER (PARTITION BY job_role) average_salary,
        COUNT(employee_id) OVER (PARTITION BY job_role) total_employees
        
    FROM employee_salary
)
SELECT 
    job_role,
    CASE 
        WHEN performance_score > 4 AND annual_salary_usd < average_salary THEN 'Underpaid'
        WHEN performance_score < 4 AND annual_salary_usd > average_salary THEN 'Overpaid'
    END AS salary_status,
    COUNT(employee_id) AS total_employees,
    total_employees,
    ROUND(AVG(num_skills), 2) AS avg_num_skills,
    ROUND(AVG(years_experience), 2) AS avg_years_experience
FROM employee_status
WHERE (performance_score > 4 AND annual_salary_usd < average_salary) 
   OR (performance_score < 4 AND annual_salary_usd > average_salary)
GROUP BY job_role, salary_status, total_employees
ORDER BY job_role, salary_status;

-- i: Untungnya yang overpaid memiliki avg num skill dan  avg experience lebih tinggi daripada underpaid, sehingga dalam kasus nyata ini adalah wajar karena standar salary masih dilihat dari beberapa aspek penting seperti skill, experience dan belakang akademik (sudah dihitung diatas) meskipun performance scorenya terhitung rendah. 

-- ===============================================================================================

-- 12. Side by side comparison: overpaid, underpaid, and fairly paid
WITH employee_status AS (
    SELECT job_role, employee_id, performance_score, num_skills, annual_salary_usd, years_experience,
        AVG(annual_salary_usd) OVER (PARTITION BY job_role) average_salary,
        COUNT(employee_id) OVER (PARTITION BY job_role) total_employees
        
    FROM employee_salary
) 
SELECT job_role,
    CASE 
        WHEN performance_score >= 4 AND annual_salary_usd < average_salary THEN  'underpaid'
        WHEN performance_score < 4 AND annual_salary_usd > average_salary THEN 'overpaid'
        WHEN performance_score < 4 AND annual_salary_usd < average_salary THEN 'fairly paid'
        WHEN performance_score >= 4 AND annual_salary_usd > average_salary THEN 'fairly paid'
        -- ELSE 'fairly paid'  <------bisa pakai ini untuk menjaring kondisi kedua terakhir
        
    END salary_status,
    COUNT(employee_id) total_employees_per_job_role, 
    total_employees,
    ROUND(AVG(num_skills), 2) avg_num_skills,
    ROUND(AVG(years_experience), 2) avg_years_experience
FROM employee_status
GROUP BY job_role, salary_status, total_employees
;

-- 13. Relation between age and annual_salary_usd

WITH avg_salary_cte AS (
    SELECT job_role, AVG(annual_salary_usd) avg_salary_by_job, COUNT(employee_id) total_employee_by_job
    FROM employee_salary_staging
    GROUP BY job_role)
    SELECT e.job_role,
    CASE WHEN e.age BETWEEN 20 AND 30 THEN 'junior'
    WHEN e.age BETWEEN 31 AND 40 THEN 'middle'
    WHEN e.age BETWEEN 41 AND 50 THEN 'senior'
    ELSE 'old man'
    END age_bracket,
    COUNT(employee_id) total_employee_by_age_bracket, total_employee_by_job,  ROUND(AVG(annual_salary_usd)) avg_salary_by_age_bracket,  ROUND(avg_salary_by_job) avg_salary_by_job, DENSE_RANK() OVER(PARTITION BY job_role ORDER BY AVG(annual_salary_usd) DESC ) ranking_by_salary
    FROM employee_salary_staging e
    JOIN avg_salary_cte a ON  e.job_role = a.job_role
    GROUP BY job_role,age_bracket, avg_salary_by_job, total_employee_by_job
    ORDER BY 6 DESC;


-- i: Range old man range 50 tahun keatas memiliki rata-rata salary tertinggi di tiap  job role.

-- ===============================================================================================

-- NEXT STEP: DATA VISUALIZATION PREPARATION
-- Membuat VIEW untuk dihubungkan ke BI Tools (Tableau, Power BI, Looker Studio, dll).
-- VIEW ini menyatukan semua feature engineering dan status kompensasi ke dalam satu tabel bersih.

CREATE OR REPLACE VIEW vw_employee_salary_analysis AS
WITH avg_salary_cte AS (
    SELECT job_role, AVG(annual_salary_usd) AS average_salary
    FROM employee_salary
    GROUP BY job_role
)
SELECT 
    e.employee_id,
    e.age,
    e.job_role,
    e.city_tier,
    e.education_level,
    e.years_experience,
    e.num_skills,
    e.performance_score,
    e.remote_work,
    e.annual_salary_usd,
    ROUND(a.average_salary, 2) AS job_role_avg_salary,
    CASE 
        WHEN e.performance_score >= 4 AND e.annual_salary_usd < a.average_salary THEN 'Underpaid'
        WHEN e.performance_score < 4 AND e.annual_salary_usd > a.average_salary THEN 'Overpaid'
        ELSE 'Fairly Paid'
    END AS salary_status
FROM employee_salary e
JOIN avg_salary_cte a ON e.job_role = a.job_role;

SELECT * FROM vw_employee_salary_analysis;
