const openSidebarBtn = document.getElementById("open-sidebar");
const closeSidebarBtn = document.getElementById("close-sidebar");
const sidebar = document.getElementById("sidebar");

openSidebarBtn.addEventListener("click", openSidebar);
closeSidebarBtn.addEventListener("click", closeSidebar);

window.addEventListener("popstate", closeSidebar);

function openSidebar() {
    sidebar.classList.add("open");
}

function closeSidebar() {
    sidebar.classList.remove("open");
}

openSidebar();
