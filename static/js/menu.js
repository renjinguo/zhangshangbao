// 移动端侧边栏切换
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.toggle('show');
            document.body.classList.toggle('sidebar-open');
        });
    }
    
    // 点击页面其他区域关闭侧边栏
    document.addEventListener('click', function(event) {
        if (sidebar && sidebar.classList.contains('show') && 
            !sidebar.contains(event.target) && 
            event.target !== sidebarToggle && 
            !sidebarToggle.contains(event.target)) {
            sidebar.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        }
    });
    
    // 窗口大小改变时重置侧边栏状态
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768 && sidebar) {
            sidebar.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        }
    });

    // 手风琴菜单功能
    const accordionToggles = document.querySelectorAll('.accordion-toggle');
    accordionToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const icon = this.querySelector('.bi-chevron-down');
            if (icon) {
                icon.classList.toggle('rotate-180');
            }
        });
    });
});

// 页面加载时初始化菜单状态
window.addEventListener('load', function() {
    const activeMenu = document.querySelector('.nav-link.active');
    if (activeMenu) {
        const parentMenu = activeMenu.closest('.collapse');
        if (parentMenu) {
            parentMenu.classList.add('show');
            const toggle = parentMenu.previousElementSibling;
            if (toggle && toggle.classList.contains('accordion-toggle')) {
                const icon = toggle.querySelector('.bi-chevron-down');
                if (icon) {
                    icon.classList.add('rotate-180');
                }
            }
        }
    }
});