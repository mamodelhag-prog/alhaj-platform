// ============== منصة الحاج في اللغة العربية ==============
// إخفاء رسائل التنبيه تلقائياً بعد 5 ثواني
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.querySelectorAll(".alert").forEach(el => {
      if (el.classList.contains("show")) {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
        bsAlert.close();
      }
    });
  }, 5000);
});

// تأكيد قبل الحذف
function confirmDelete(message) {
  return confirm(message || "متأكد من الحذف؟");
}

// فتح/إغلاق القائمة الجانبية في الموبايل
function setupSidebar() {
  const sidebar = document.getElementById("sidebar");
  const open = document.getElementById("openSidebar");
  const close = document.getElementById("closeSidebar");
  if (open) open.addEventListener("click", () => sidebar.classList.add("open"));
  if (close) close.addEventListener("click", () => sidebar.classList.remove("open"));
}
setupSidebar();
