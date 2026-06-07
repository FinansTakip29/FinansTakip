(function () {
    const storageKey = "finanstakip-theme";
    const installStorageKey = "finanstakip-install-dismissed";
    const root = document.documentElement;
    const toggleButton = document.querySelector("[data-theme-toggle]");
    const splash = document.querySelector("[data-app-splash]");
    const installCard = document.querySelector("[data-pwa-install-card]");
    const installButton = document.querySelector("[data-pwa-install]");
    const dismissButton = document.querySelector("[data-pwa-dismiss]");
    const installCopy = document.querySelector("[data-pwa-install-copy]");
    let deferredInstallPrompt = null;
    let dashboardCharts = [];

    window.addEventListener("load", function () {
        if (splash) {
            splash.classList.add("app-splash-hidden");
        }
    });

    if ("serviceWorker" in navigator) {
        window.addEventListener("load", function () {
            navigator.serviceWorker.register("/service-worker.js", { scope: "/" }).catch(function () {
                // PWA kaydı desteklenmeyen ortamlarda sessizce geçilir.
            });
        });
    }

    function isStandalone() {
        return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
    }

    function isIosSafari() {
        const ua = window.navigator.userAgent.toLowerCase();
        return /iphone|ipad|ipod/.test(ua) && /safari/.test(ua) && !/crios|fxios|edgios/.test(ua);
    }

    function showInstallCard(copy) {
        if (!installCard || isStandalone() || localStorage.getItem(installStorageKey) === "1") {
            return;
        }
        if (installCopy && copy) {
            installCopy.textContent = copy;
        }
        installCard.hidden = false;
    }

    window.addEventListener("beforeinstallprompt", function (event) {
        event.preventDefault();
        deferredInstallPrompt = event;
        showInstallCard("Uygulamayı ana ekranına ekleyip tam ekran kullan.");
    });

    if (isIosSafari()) {
        showInstallCard("Safari paylaş menüsünden Ana Ekrana Ekle seçeneğini kullan.");
        if (installButton) {
            installButton.hidden = true;
        }
    }

    if (installButton) {
        installButton.addEventListener("click", async function () {
            if (!deferredInstallPrompt) {
                return;
            }
            deferredInstallPrompt.prompt();
            await deferredInstallPrompt.userChoice;
            deferredInstallPrompt = null;
            if (installCard) {
                installCard.hidden = true;
            }
        });
    }

    if (dismissButton) {
        dismissButton.addEventListener("click", function () {
            localStorage.setItem(installStorageKey, "1");
            if (installCard) {
                installCard.hidden = true;
            }
        });
    }

    function applyTheme(theme) {
        root.dataset.theme = theme;
        if (toggleButton) {
            const icon = toggleButton.querySelector("i");
            const label = toggleButton.querySelector("span");
            if (icon) {
                icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
            }
            if (label) {
                label.textContent = theme === "dark" ? "Light" : "Dark";
            }
        }
    }

    const savedTheme = localStorage.getItem(storageKey) || "light";
    applyTheme(savedTheme);

    if (toggleButton) {
        toggleButton.addEventListener("click", function () {
            const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
            localStorage.setItem(storageKey, nextTheme);
            applyTheme(nextTheme);
            renderDashboardCharts();
        });
    }

    function cssVar(name) {
        return getComputedStyle(root).getPropertyValue(name).trim();
    }

    function chartTextColor() {
        return cssVar("--app-muted") || "#64748b";
    }

    function chartGridColor() {
        return cssVar("--app-border") || "#e5e7eb";
    }

    function renderDashboardCharts() {
        if (!window.Chart || !window.FinansTakipCharts) {
            return;
        }

        const chartData = window.FinansTakipCharts;
        const trendCanvas = document.getElementById("trendChart");
        const categoryCanvas = document.getElementById("categoryChart");
        const textColor = chartTextColor();
        const gridColor = chartGridColor();

        dashboardCharts.forEach(function (chart) {
            chart.destroy();
        });
        dashboardCharts = [];

        if (trendCanvas) {
            dashboardCharts.push(new Chart(trendCanvas, {
                type: "line",
                data: {
                    labels: chartData.trendLabels || [],
                    datasets: [
                        {
                            label: "Gelir",
                            data: chartData.trendIncome || [],
                            borderColor: "#16a34a",
                            backgroundColor: "rgba(22, 163, 74, .12)",
                            borderWidth: 2,
                            tension: .35,
                            fill: true
                        },
                        {
                            label: "Gider",
                            data: chartData.trendExpense || [],
                            borderColor: "#dc2626",
                            backgroundColor: "rgba(220, 38, 38, .10)",
                            borderWidth: 2,
                            tension: .35,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: textColor, boxWidth: 12, usePointStyle: true }
                        }
                    },
                    scales: {
                        x: { ticks: { color: textColor }, grid: { color: gridColor } },
                        y: { beginAtZero: true, ticks: { color: textColor }, grid: { color: gridColor } }
                    }
                }
            }));
        }

        if (categoryCanvas) {
            const labels = chartData.categoryLabels && chartData.categoryLabels.length ? chartData.categoryLabels : ["Kayıt yok"];
            const values = chartData.categoryValues && chartData.categoryValues.length ? chartData.categoryValues : [1];
            dashboardCharts.push(new Chart(categoryCanvas, {
                type: "doughnut",
                data: {
                    labels,
                    datasets: [{
                        data: values,
                        backgroundColor: ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2"],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "68%",
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: { color: textColor, boxWidth: 12, usePointStyle: true }
                        }
                    }
                }
            }));
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", renderDashboardCharts);
    } else {
        renderDashboardCharts();
    }
})();
