"use strict";


function initializeMobileMenu() {
    const menuButton = document.getElementById("menuButton");
    const mainNav = document.getElementById("mainNav");

    if (!menuButton || !mainNav) {
        return;
    }

    menuButton.addEventListener("click", function () {
        const menuIsOpen = mainNav.classList.toggle("open");

        menuButton.setAttribute(
            "aria-expanded",
            String(menuIsOpen)
        );
    });

    const navigationLinks = mainNav.querySelectorAll("a");

    navigationLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            mainNav.classList.remove("open");

            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );
        });
    });

    document.addEventListener("click", function (event) {
        const clickedInsideMenu = mainNav.contains(event.target);
        const clickedMenuButton = menuButton.contains(event.target);

        if (!clickedInsideMenu && !clickedMenuButton) {
            mainNav.classList.remove("open");

            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            mainNav.classList.remove("open");

            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );

            menuButton.focus();
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 900) {
            mainNav.classList.remove("open");

            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });
}


function initializeCurrentYear() {
    const currentYear = document.getElementById("currentYear");

    if (!currentYear) {
        return;
    }

    currentYear.textContent = new Date().getFullYear();
}


function normalizePath(path) {
    if (!path) {
        return "/";
    }

    let normalizedPath = path.split("?")[0].split("#")[0];

    if (!normalizedPath.startsWith("/")) {
        normalizedPath = "/" + normalizedPath;
    }

    if (
        normalizedPath.length > 1 &&
        !normalizedPath.endsWith("/")
    ) {
        normalizedPath += "/";
    }

    return normalizedPath;
}


function setActiveNavigationLink() {
    const currentPath = normalizePath(
        window.location.pathname
    );

    const navigationLinks =
        document.querySelectorAll(".main-nav a");

    navigationLinks.forEach(function (link) {
        const href = link.getAttribute("href");

        if (
            !href ||
            href.startsWith("#") ||
            href.startsWith("javascript:") ||
            href.startsWith("mailto:") ||
            href.startsWith("tel:")
        ) {
            return;
        }

        let linkPath;

        try {
            const linkUrl = new URL(
                href,
                window.location.origin
            );

            linkPath = normalizePath(linkUrl.pathname);
        } catch (error) {
            return;
        }

        link.classList.remove("active");

        if (linkPath === currentPath) {
            link.classList.add("active");
        }
    });
}


function initializeComponents() {
    initializeMobileMenu();
    initializeCurrentYear();
    setActiveNavigationLink();
}


if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        initializeComponents
    );
} else {
    initializeComponents();
}