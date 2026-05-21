from flask import Blueprint, render_template, jsonify, current_app
import time
import math
import hashlib
import os

stress_bp = Blueprint("stress", __name__)


def _cpu_burn(duration_seconds: float = 5.0):
    """Lakukan komputasi berat selama `duration_seconds` detik untuk naikkan CPU."""
    deadline = time.time() + duration_seconds
    result = 0
    while time.time() < deadline:
        # Hash loop + sqrt loop — murni CPU-bound
        for i in range(5000):
            result += math.sqrt(i) * math.log(i + 1)
            hashlib.sha256(str(result).encode()).hexdigest()
    return result


@stress_bp.route("/stress")
def stress():
    """
    Endpoint CPU-heavy untuk trigger Kubernetes HPA.
    Jalankan komputasi berat selama 5 detik per request.
    Load generator menembak endpoint ini berulang kali untuk menaikkan CPU > 50%.
    """
    school_name = current_app.config.get("SCHOOL_NAME")
    start = time.time()
    _cpu_burn(duration_seconds=5.0)
    elapsed = round(time.time() - start, 2)
    pod_name = os.environ.get("HOSTNAME", "local")
    return render_template(
        "stress.html",
        school_name=school_name,
        elapsed=elapsed,
        pod_name=pod_name,
    )


@stress_bp.route("/stress/api")
def stress_api():
    """
    Versi JSON dari /stress — dipakai load generator (curl/wrk/locust).
    Mengembalikan info pod dan waktu eksekusi.
    """
    start = time.time()
    _cpu_burn(duration_seconds=5.0)
    elapsed = round(time.time() - start, 2)
    pod_name = os.environ.get("HOSTNAME", "local")
    return jsonify({
        "status": "ok",
        "pod": pod_name,
        "elapsed_seconds": elapsed,
        "message": "CPU stress selesai. Cek kubectl get hpa untuk melihat scaling."
    })


@stress_bp.route("/health")
def health():
    """Health check endpoint untuk Kubernetes liveness/readiness probe."""
    return jsonify({"status": "healthy", "service": "sekolah-cahaya-utama"})
