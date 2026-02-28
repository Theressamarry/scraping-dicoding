import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


def get_total_pages(base_url):
    """Ambil total halaman dari pagination. Kalau gagal, fallback ke 1."""
    try:
        response = requests.get(f"{base_url}?page=1", timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        pagination_links = soup.find_all("a", href=re.compile(r"page=\d+"))

        page_numbers = []

        for link in pagination_links:
            href = link.get("href", "")
            match = re.search(r"page=(\d+)", href)
            if match:
                page_numbers.append(int(match.group(1)))

        if page_numbers:
            return max(page_numbers)
        return 1

    except Exception as e:
        print("Gagal ambil total halaman:", e)
        return 1


def scrape_dicoding_offering(max_pages=None):
    all_data = []
    base_url = "https://www.dicoding.com/codingcamp/offering"

    # Kalau tidak diisi, hitung otomatis dari pagination.
    if max_pages is None:
        print("Cek jumlah halaman dulu...")
        max_pages = get_total_pages(base_url)
        print("Total halaman:", max_pages)

    print("\nMulai ambil data...\n")

    for page in range(1, max_pages + 1):
        try:
            url = f"{base_url}?page={page}"
            print(f"Proses halaman {page}/{max_pages}")

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table")

            if not table:
                print("Tabel tidak ditemukan di halaman ini")
                continue

            rows = table.find_all("tr")
            for row in rows[1:]:
                cols = row.find_all("td")

                if len(cols) >= 3:
                    no = cols[0].text.strip()
                    nama = cols[1].text.strip()
                    sekolah = cols[2].text.strip()

                    if no and nama and sekolah:
                        all_data.append({
                            "No": no,
                            "Nama Siswa": nama,
                            "Asal Sekolah/Universitas": sekolah
                        })

            print("Selesai halaman", page)
            time.sleep(1)

        except requests.RequestException as e:
            print("Request error di halaman", page, ":", e)

        except Exception as e:
            print("Error parsing di halaman", page, ":", e)

    return pd.DataFrame(all_data)


if __name__ == "__main__":
    # Jalankan scraping
    df = scrape_dicoding_offering()

    print("\n==============================")
    print("Total data yang didapat:", len(df))
    print("==============================\n")

    print("Preview data:")
    print(df.head(10).to_string(index=False))

    csv_file = "dicoding_offering_data.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print("\nData disimpan ke:", csv_file)

    # Coba simpan juga ke Excel.
    excel_file = "dicoding_offering_data.xlsx"
    try:
        df.to_excel(excel_file, index=False, engine="openpyxl")
        print("Data disimpan ke:", excel_file)
    except Exception as e:
        print("Lewat simpan Excel karena ada error:", e)

    print("\n==============================")
    print("Data dari Universitas Pembangunan Nasional Veteran Jawa Timur:")
    print("==============================")
    upn_veteran = df[
        df["Asal Sekolah/Universitas"].str.contains(
            "Universitas Pembangunan Nasional Veteran Jawa Timur", case=False, na=False
        )
    ]
    
    if len(upn_veteran) > 0:
        for _, row in upn_veteran.iterrows():
            print(f"{row['No']}. {row['Nama Siswa']}")
        print(f"\nTotal: {len(upn_veteran)} orang")
    else:
        print("Tidak ada data dari universitas tersebut")
