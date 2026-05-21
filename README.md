# 🌍 SDGs Poin 13: Aplikasi Kalkulator Jejak Karbon Kampus (Kubernetes Project)

Proyek ini dibuat untuk memenuhi **Evaluasi 3 - Praktikum Komputasi Awan**. Aplikasi berbasis Web ini bertujuan untuk mengedukasi mahasiswa mengenai estimasi emisi karbon harian yang dihasilkan dari moda transportasi menuju kampus, sebagai bentuk dukungan terhadap gerakan *Sustainable Development Goals (SDGs) No. 13: Climate Action*.

## 🚀 Fitur Utama Arsitektur (Kubernetes)
- **ConfigMap:** Manajemen konfigurasi nama aplikasi secara dinamis.
- **High Availability Deployment:** Menjaga aplikasi tetap menyala dengan replikasi minimum 2 Pod yang tersebar di multi-node cluster.
- **NodePort Service:** Penyeimbang beban (Load Balancer) internal yang mendistribusikan trafik di port `30080`.
- **Horizontal Pod Autoscaler (HPA):** Mekanisme *auto-scaling* otomatis yang akan menambah jumlah Pod (hingga maks 5 Pod) ketika penggunaan CPU melewati ambang batas 50%.

## 📂 Struktur Repositori
```text
├── kubernetes/
│   └── k8s-manifests.yaml   # Manifest terpadu (ConfigMap, Deployment, Service, HPA)
├── app.py                   # Aplikasi web Python Flask
├── Dockerfile               # Dokumen instruksi build Docker Image
└── README.md                # Dokumentasi petunjuk penggunaan