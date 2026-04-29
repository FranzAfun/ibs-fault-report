class App {
  init() {
    this.initComponents();
    this.initPreloader();
    this.initPortletCard();
    this.initMultiDropdown();
    this.initFormValidation();
    this.initCounter();
    this.initCodePreview();
    this.initToggle();
    this.initDismissible();
    this.initLeftSidebar();
    this.initTopbarMenu();
  }

  initComponents() {
    // Initialize Lucide icons if available
    if (typeof lucide.createIcons === "function") {
      lucide.createIcons();
    }

    // Initialize Bootstrap components
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => new bootstrap.Popover(el));
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
    document.querySelectorAll(".offcanvas").forEach(el => new bootstrap.Offcanvas(el));
    document.querySelectorAll(".toast").forEach(el => new bootstrap.Toast(el));
  }

  initPreloader() {
    window.addEventListener("load", () => {
      const status = document.getElementById("status");
      const preloader = document.getElementById("preloader");

      if (status) status.style.display = "none";
      if (preloader) {
        setTimeout(() => {
          preloader.style.display = "none";
        }, 350);
      }
    });
  }

  initPortletCard() {
    // Close card
    $('[data-action="card-close"]').on("click", function (e) {
      e.preventDefault();
      const $card = $(this).closest(".card");
      $card.fadeOut(300, () => $card.remove());
    });

    // Toggle card collapse
    $('[data-action="card-toggle"]').on("click", function (e) {
      e.preventDefault();
      const $card = $(this).closest(".card");
      const $icon = $(this).find("i").eq(0);
      const $body = $card.find(".card-body");
      const $footer = $card.find(".card-footer");

      $body.slideToggle(300);
      $footer.slideToggle(200);
      $icon.toggleClass("ti-chevron-up ti-chevron-down");
      $card.toggleClass("card-collapse");
    });

    // Refresh card with spinner
    const refreshButtons = document.querySelectorAll('[data-action="card-refresh"]');
    refreshButtons.forEach(button => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        const card = e.target.closest(".card");
        let overlay = card.querySelector(".card-overlay");

        if (!overlay) {
          overlay = document.createElement("div");
          overlay.classList.add("card-overlay");
          const spinner = document.createElement("div");
          spinner.classList.add("spinner-border", "text-primary");
          overlay.appendChild(spinner);
          card.appendChild(overlay);
        }

        overlay.style.display = "flex";
        setTimeout(() => {
          overlay.style.display = "none";
        }, 1500);
      });
    });

    // Code collapse toggle
    $('[data-action="code-collapse"]').on("click", function (e) {
      e.preventDefault();
      const $card = $(this).closest(".card");
      const $icon = $(this).find("i").eq(0);
      $card.find(".code-body").slideToggle(300);
      $icon.toggleClass("ti-chevron-up ti-chevron-down");
    });
  }

  initMultiDropdown() {
    $(".dropdown-menu a.dropdown-toggle").on("click", function () {
      const $submenu = $(this).next(".dropdown-menu");
      const $parentMenu = $(this).parent().parent().find(".dropdown-menu").not($submenu);

      $parentMenu.removeClass("show");
      $parentMenu.parent().find(".dropdown-toggle").removeClass("show");
      return false;
    });
  }

  initFormValidation() {
    document.querySelectorAll(".needs-validation").forEach(form => {
      form.addEventListener("submit", e => {
        if (!form.checkValidity()) {
          e.preventDefault();
          e.stopPropagation();
        }
        form.classList.add("was-validated");
      }, false);
    });
  }

  initCounter() {
    const counters = document.querySelectorAll("[data-target]");
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = entry.target;
          let endValue = parseFloat(target.getAttribute("data-target").replace(/,/g, ""));
          let current = 0;
          const increment = endValue / 25;
          const isInteger = Number.isInteger(endValue);

          const formatNumber = (num) => {
            return isInteger
              ? num.toLocaleString()
              : num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
          };

          const animate = () => {
            if (current < endValue) {
              current += increment;
              if (current > endValue) current = endValue;
              target.innerText = formatNumber(current);
              requestAnimationFrame(animate);
            } else {
              target.innerText = formatNumber(endValue);
            }
          };

          animate();
          observer.unobserve(target);
        }
      });
    }, { threshold: 1 });

    counters.forEach(counter => observer.observe(counter));
  }

  initCodePreview() {
    if (typeof Prism !== "undefined" && Prism.plugins && Prism.plugins.NormalizeWhitespace) {
      Prism.plugins.NormalizeWhitespace.setDefaults({
        "remove-trailing": true,
        "remove-indent": true,
        "left-trim": true,
        "right-trim": true,
        "tabs-to-spaces": 4,
        "spaces-to-tabs": 4
      });
    }
  }

  initToggle() {
    document.querySelectorAll("[data-toggler]").forEach(container => {
      const onEl = container.querySelector("[data-toggler-on]");
      const offEl = container.querySelector("[data-toggler-off]");
      let isOn = container.getAttribute("data-toggler") === "on";

      const update = () => {
        if (isOn) {
          onEl?.classList.remove("d-none");
          offEl?.classList.add("d-none");
        } else {
          onEl?.classList.add("d-none");
          offEl?.classList.remove("d-none");
        }
      };

      onEl?.addEventListener("click", () => {
        isOn = false;
        update();
      });

      offEl?.addEventListener("click", () => {
        isOn = true;
        update();
      });

      update();
    });
  }

  initDismissible() {
    document.querySelectorAll("[data-dismissible]").forEach(btn => {
      btn.addEventListener("click", () => {
        const selector = btn.getAttribute("data-dismissible");
        const target = document.querySelector(selector);
        if (target) target.remove();
      });
    });
  }

  initLeftSidebar() {
    const sideNav = document.querySelector(".side-nav");
    if (!sideNav) return;

    // Prevent default collapse behavior
    sideNav.querySelectorAll("li [data-bs-toggle='collapse']").forEach(link => {
      link.addEventListener("click", e => e.preventDefault());
    });

    const collapses = sideNav.querySelectorAll("li .collapse");
    const currentPath = window.location.href.split(/[?#]/)[0];

    // Close other collapses when one opens
    collapses.forEach(collapse => {
      collapse.addEventListener("show.bs.collapse", e => {
        const target = e.target;
        const siblings = [];
        let parent = target.parentElement;

        while (parent && parent !== sideNav) {
          if (parent.classList.contains("collapse")) siblings.push(parent);
          parent = parent.parentElement;
        }

        collapses.forEach(col => {
          if (col !== target && !siblings.includes(col)) {
            new bootstrap.Collapse(col, { toggle: false }).hide();
          }
        });
      });
    });

    // Highlight active menu item
    sideNav.querySelectorAll("a").forEach(link => {
      if (link.href === currentPath) {
        sideNav.querySelectorAll("a.active, li.active, .collapse.show").forEach(el => {
          el.classList.remove("active", "show");
        });

        link.classList.add("active");
        let li = link.closest("li");
        while (li && li !== sideNav) {
          li.classList.add("active");
          const collapse = li.closest(".collapse");
          if (collapse) {
            new bootstrap.Collapse(collapse, { toggle: false }).show();
            const parentLi = collapse.closest("li");
            if (parentLi) parentLi.classList.add("active");
          }
          li = collapse ? collapse.closest("li") : li.parentElement;
        }
      }
    });

    // Auto-scroll to active item
    setTimeout(() => {
      const activeLink = sideNav.querySelector("li.active .active");
      const scrollWrapper = document.querySelector(".sidenav-menu .simplebar-content-wrapper");
      if (activeLink && scrollWrapper) {
        const topPos = activeLink.offsetTop - 300;
        if (topPos > 100) {
          const start = scrollWrapper.scrollTop;
          const distance = topPos - start;
          let startTime = null;
          const duration = 600;

          const animation = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const elapsed = currentTime - startTime;
            const progress = elapsed / (duration / 2);

            if (progress < 1) {
              scrollWrapper.scrollTop = (distance / 2) * progress * progress + start;
            } else {
              const t = progress - 1;
              scrollWrapper.scrollTop = -(distance / 2) * (t * (t - 2) - 1) + start;
            }

            if (elapsed < duration) {
              setTimeout(animation, 20);
            }
          };

          animation();
        }
      }
    }, 200);
  }

  initTopbarMenu() {
    const navbar = document.querySelector(".navbar-nav");
    if (!navbar) return;

    const currentPath = window.location.href.split(/[?#]/)[0];

    // Highlight active topbar item
    navbar.querySelectorAll("li a").forEach(link => {
      if (link.href === currentPath) {
        link.classList.add("active");
        let parent = link.parentElement;
        for (let i = 0; i < 6 && parent && parent !== document.body; i++) {
          if (parent.tagName === "LI" || parent.classList.contains("dropdown")) {
            parent.classList.add("active");
          }
          parent = parent.parentElement;
        }
      }
    });

    // Mobile menu toggle
    const toggleBtn = document.querySelector(".navbar-toggle");
    const navigation = document.getElementById("navigation");

    if (toggleBtn && navigation) {
      toggleBtn.addEventListener("click", () => {
        toggleBtn.classList.toggle("open");
        navigation.style.display = navigation.style.display === "block" ? "none" : "block";
      });
    }
  }
}

// Skin Presets
const skinPresets = {
  classic: { theme: "light", topbar: "light", menu: "dark", sidenav: { user: true } },
  modern: { theme: "light", topbar: "light", menu: "gradient", sidenav: { user: true } },
  material: { theme: "light", topbar: "dark", menu: "light", sidenav: { user: true } },
  saas: { theme: "light", topbar: "light", menu: "dark", sidenav: { user: true } },
  minimal: { theme: "light", topbar: "light", menu: "gray", sidenav: { user: false } },
  flat: { theme: "light", topbar: "light", menu: "dark", sidenav: { user: false } }
};

class LayoutCustomizer {
  constructor() {
    this.html = document.documentElement;
    this.config = {};
  }

  init() {
    this.initConfig();
    this.initSwitchListener();
    this.initWindowSize();
    this._adjustLayout();
    this.setSwitchFromConfig();
    this.openCustomizer();
  }

  initConfig() {
    this.defaultConfig = JSON.parse(JSON.stringify(window.defaultConfig));
    this.config = JSON.parse(JSON.stringify(window.config));
    this.setSwitchFromConfig();
  }

  isFirstVisit() {
    if (!localStorage.getItem("__user_has_visited__")) {
      localStorage.setItem("__user_has_visited__", "true");
      return true;
    }
    return false;
  }

  openCustomizer() {
    const offcanvas = document.getElementById("theme-settings-offcanvas");
    if (offcanvas && this.isFirstVisit()) {
      const bsOffcanvas = new bootstrap.Offcanvas(offcanvas);
      setTimeout(() => bsOffcanvas.show(), 1000);
    }
  }

  applyPreset(presetName) {
    const preset = skinPresets[presetName];
    if (!preset) return;

    if (preset.theme) {
      this.config.theme = preset.theme;
      this.html.setAttribute("data-bs-theme", preset.theme);
    }
    if (preset.topbar) {
      this.config.topbar.color = preset.topbar;
      this.html.setAttribute("data-topbar-color", preset.topbar);
    }
    if (preset.menu) {
      this.config.menu.color = preset.menu;
      this.html.setAttribute("data-menu-color", preset.menu);
    }
    if (preset.sidenav?.size) {
      this.config.sidenav.size = preset.sidenav.size;
      this.html.setAttribute("data-sidenav-size", preset.sidenav.size);
    }
    if (preset.sidenav?.user !== undefined) {
      this.config.sidenav.user = preset.sidenav.user;
      preset.sidenav.user
        ? this.html.setAttribute("data-sidenav-user", "true")
        : this.html.removeAttribute("data-sidenav-user");
    }
  }

  changeSkin(skin) {
    this.config.skin = skin;
    this.html.setAttribute("data-skin", skin);
    this.applyPreset(skin);
    this.setSwitchFromConfig();
  }

  changeMenuColor(color) {
    this.config.menu.color = color;
    this.html.setAttribute("data-menu-color", color);
    this.setSwitchFromConfig();
  }

  changeLeftbarSize(size, updateConfig = true) {
    this.html.setAttribute("data-sidenav-size", size);
    if (updateConfig) {
      this.config.sidenav.size = size;
      this.setSwitchFromConfig();
    }
  }

  changeLayoutPosition(position) {
    this.config.layout.position = position;
    this.html.setAttribute("data-layout-position", position);
    this.setSwitchFromConfig();
  }

  getSystemTheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  changeTheme(theme) {
    if (theme === "system") theme = this.getSystemTheme();
    this.config.theme = theme;
    this.html.setAttribute("data-bs-theme", theme);
    this.setSwitchFromConfig();
  }

  changeTopbarColor(color) {
    this.config.topbar.color = color;
    this.html.setAttribute("data-topbar-color", color);
    this.setSwitchFromConfig();
  }

  changeSidebarUser(show) {
    this.config.sidenav.user = show;
    show
      ? this.html.setAttribute("data-sidenav-user", "true")
      : this.html.removeAttribute("data-sidenav-user");
    this.setSwitchFromConfig();
  }

  resetTheme() {
    this.config = JSON.parse(JSON.stringify(window.defaultConfig));
    this.changeSkin(this.config.skin);
    this.changeMenuColor(this.config.menu.color);
    this.changeLeftbarSize(this.config.sidenav.size);
    this.changeTheme(this.config.theme);
    this.changeLayoutPosition(this.config.layout.position);
    this.changeTopbarColor(this.config.topbar.color);
    this.changeSidebarUser(this.config.sidenav.user);
    this._adjustLayout();
  }

  setSwitchFromConfig() {
    const config = this.config;
    sessionStorage.setItem("__INSPINIA_CONFIG__", JSON.stringify(config));

    document.querySelectorAll("#theme-settings-offcanvas input[type=radio]").forEach(radio => radio.checked = false);

    const setRadio = (selector, value) => {
      const el = document.querySelector(selector);
      if (el) el.checked = value;
    };

    setRadio('input[name="sidebar-user"]', config.sidenav.user === true);

    [
      ["data-skin", config.skin],
      ["data-bs-theme", config.theme],
      ["data-layout-position", config.layout.position],
      ["data-topbar-color", config.topbar.color],
      ["data-menu-color", config.menu.color],
      ["data-sidenav-size", config.sidenav.size]
    ].forEach(([attr, value]) => {
      const radio = document.querySelector(`input[name="${attr}"][value="${value}"]`);
      if (radio) radio.checked = true;
    });
  }

  initSwitchListener() {
    const bindChange = (selector, callback) => {
      document.querySelectorAll(selector).forEach(el => {
        el.addEventListener("change", () => callback(el));
      });
    };

    bindChange('input[name="data-skin"]', el => this.changeSkin(el.value));
    bindChange('input[name="data-bs-theme"]', el => this.changeTheme(el.value));
    bindChange('input[name="data-menu-color"]', el => this.changeMenuColor(el.value));
    bindChange('input[name="data-sidenav-size"]', el => this.changeLeftbarSize(el.value));
    bindChange('input[name="data-layout-position"]', el => this.changeLayoutPosition(el.value));
    bindChange('input[name="data-topbar-color"]', el => this.changeTopbarColor(el.value));
    bindChange('input[name="sidebar-user"]', el => this.changeSidebarUser(el.checked));

    // Light/Dark toggle
    const modeToggle = document.getElementById("light-dark-mode");
    if (modeToggle) {
      modeToggle.addEventListener("click", () => {
        const newTheme = this.config.theme === "light" ? "dark" : "light";
        this.changeTheme(newTheme);
      });
    }

    // Reset button
    const resetBtn = document.querySelector("#reset-layout");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => this.resetTheme());
    }

    // Sidebar toggle
    const sidebarToggle = document.querySelector(".sidenav-toggle-button");
    if (sidebarToggle) {
      sidebarToggle.addEventListener("click", () => this._toggleSidebar());
    }

    // Close offcanvas
    const closeBtn = document.querySelector(".button-close-offcanvas");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        this.html.classList.remove("sidebar-enable");
        this.hideBackdrop();
      });
    }

    // Hover mode toggle
    document.querySelectorAll(".button-on-hover").forEach(btn => {
      btn.addEventListener("click", () => {
        const current = this.html.getAttribute("data-sidenav-size");
        this.changeLeftbarSize(current === "on-hover-active" ? "on-hover" : "on-hover-active", true);
      });
    });
  }

  _toggleSidebar() {
    const currentSize = this.html.getAttribute("data-sidenav-size");
    const configSize = this.config.sidenav.size;

    if (currentSize === "offcanvas") {
      this.showBackdrop();
    } else if (configSize === "compact") {
      this.changeLeftbarSize(currentSize === "condensed" ? "compact" : "condensed", false);
    } else {
      this.changeLeftbarSize(currentSize === "condensed" ? "default" : "condensed", true);
    }

    this.html.classList.toggle("sidebar-enable");
  }

  showBackdrop() {
    const backdrop = document.createElement("div");
    backdrop.id = "custom-backdrop";
    backdrop.className = "offcanvas-backdrop fade show";
    document.body.appendChild(backdrop);
    document.body.style.overflow = "hidden";
    if (window.innerWidth > 767) {
      document.body.style.paddingRight = "15px";
    }

    backdrop.addEventListener("click", () => {
      this.html.classList.remove("sidebar-enable");
      this.hideBackdrop();
    });
  }

  hideBackdrop() {
    const backdrop = document.getElementById("custom-backdrop");
    if (backdrop) {
      document.body.removeChild(backdrop);
      document.body.style.overflow = "";
      document.body.style.paddingRight = "";
    }
  }

  _adjustLayout() {
    const width = window.innerWidth;
    const size = this.config.sidenav.size;

    if (width <= 767.98) {
      this.changeLeftbarSize("offcanvas", false);
    } else if (width <= 1140 && !["offcanvas"].includes(size)) {
      this.changeLeftbarSize("condensed", false);
    } else {
      this.changeLeftbarSize(size);
    }
  }

  initWindowSize() {
    window.addEventListener("resize", () => this._adjustLayout());
  }
}

class Plugins {
  init() {
    this.initFlatPicker();
    this.initTouchSpin();
  }

  initFlatPicker() {
    document.querySelectorAll("[data-provider]").forEach(el => {
      const provider = el.getAttribute("data-provider");
      const attrs = el.attributes;
      const options = { disableMobile: true, defaultDate: new Date() };

      if (provider === "flatpickr") {
        if (attrs["data-date-format"]) options.dateFormat = attrs["data-date-format"].value;
        if (attrs["data-enable-time"]) {
          options.enableTime = true;
          options.dateFormat += " H:i";
        }
        if (attrs["data-altFormat"]) {
          options.altInput = true;
          options.altFormat = attrs["data-altFormat"].value;
        }
        if (attrs["data-minDate"]) options.minDate = attrs["data-minDate"].value;
        if (attrs["data-maxDate"]) options.maxDate = attrs["data-maxDate"].value;
        if (attrs["data-default-date"]) options.defaultDate = attrs["data-default-date"].value;
        if (attrs["data-multiple-date"]) options.mode = "multiple";
        if (attrs["data-range-date"]) options.mode = "range";
        if (attrs["data-inline-date"]) {
          options.inline = true;
          options.defaultDate = attrs["data-default-date"].value;
        }
        if (attrs["data-disable-date"]) {
          options.disable = attrs["data-disable-date"].value.split(",");
        }
        if (attrs["data-week-number"]) options.weekNumbers = true;

        flatpickr(el, options);
      }

      if (provider === "timepickr") {
        const timeOptions = {
          enableTime: true,
          noCalendar: true,
          dateFormat: "H:i",
          defaultDate: new Date()
        };
        if (attrs["data-time-hrs"]) timeOptions.time_24hr = true;
        if (attrs["data-min-time"]) timeOptions.minTime = attrs["data-min-time"].value;
        if (attrs["data-max-time"]) timeOptions.maxTime = attrs["data-max-time"].value;
        if (attrs["data-default-time"]) timeOptions.defaultDate = attrs["data-default-time"].value;
        if (attrs["data-time-inline"]) {
          timeOptions.inline = true;
          timeOptions.defaultDate = attrs["data-time-inline"].value;
        }
        flatpickr(el, timeOptions);
      }
    });
  }

  initTouchSpin() {
    document.querySelectorAll("[data-touchspin]").forEach(container => {
      const minus = container.querySelector("[data-minus]");
      const plus = container.querySelector("[data-plus]");
      const input = container.querySelector("input");

      if (!input) return;

      const min = Number(input.min);
      const max = Number(input.max ?? 0);
      const hasMin = Number.isFinite(min);
      const hasMax = Number.isFinite(max);

      const getValue = () => Number.parseInt(input.value) || 0;

      if (!input.hasAttribute("readonly")) {
        minus?.addEventListener("click", () => {
          const val = getValue() - 1;
          if (!hasMin || val >= min) input.value = val.toString();
        });

        plus?.addEventListener("click", () => {
          const val = getValue() + 1;
          if (!hasMax || val <= max) input.value = val.toString();
        });
      }
    });
  }
}


// Utility: Get CSS variable
const ins = (name, alpha = 1) => {
  const value = getComputedStyle(document.documentElement).getPropertyValue(`--ins-${name}`).trim();
  return name.includes("-rgb") ? `rgba(${value}, ${alpha})` : value;
};

// Debounce utility
function debounce(func, wait) {
  let timeout;
  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(func, wait);
  };
}

// ApexCharts Wrapper
class CustomApexChart {
  static instances = [];

  constructor({ selector, series = [], options: getOptions = {}, colors = [] }) {
    if (!selector) {
      console.warn("CustomApexChart: 'selector' is required.");
      return;
    }

    this.selector = selector;
    this.series = series;
    this.getOptions = getOptions;
    this.colors = colors;
    this.element = selector instanceof HTMLElement ? selector : document.querySelector(selector);
    this.chart = null;

    try {
      this.render();
      CustomApexChart.instances.push(this);
    } catch (err) {
      console.error("CustomApexChart: Error during chart initialization:", err);
    }
  }

  getColors() {
    const options = this.getOptions();
    if (options?.colors?.length) return options.colors;

    if (this.element) {
      const dataColors = this.element.getAttribute("data-colors");
      if (dataColors) {
        return dataColors.split(",").map(c => c.trim()).map(c => c.startsWith("#") || c.includes("rgb") ? c : ins(c));
      }
    }

    return [ins("primary"), ins("secondary"), ins("danger")];
  }

  render() {
    if (this.chart) this.chart.destroy();
    if (!this.element) {
      console.warn(`CustomApexChart: No element found for selector '${this.selector}'.`);
      return;
    }

    const options = JSON.parse(JSON.stringify(this.getOptions()));
    options.colors = this.getColors();
    this.injectDynamicColors(options, options.colors);
    options.series = options.series || this.series;

    this.chart = new ApexCharts(this.element, options);
    this.chart.render();
  }

  injectDynamicColors(options, colors) {
    if (options.chart?.type?.toLowerCase() === "boxplot") {
      options.plotOptions = options.plotOptions || {};
      options.plotOptions.boxPlot = options.plotOptions.boxPlot || {};
      options.plotOptions.boxPlot.colors = options.plotOptions.boxPlot.colors || {};
      options.plotOptions.boxPlot.colors.upper = options.plotOptions.boxPlot.colors.upper || colors[0];
      options.plotOptions.boxPlot.colors.lower = options.plotOptions.boxPlot.colors.lower || colors[1];
    }

    if (Array.isArray(options.yaxis)) {
      options.yaxis.forEach((axis, i) => {
        const color = colors[i] || this.colors[i] || "#999";
        axis.axisBorder = axis.axisBorder || {};
        axis.axisBorder.color = color;
        axis.labels = axis.labels || {};
        axis.labels.style = axis.labels.style || {};
        axis.labels.style.color = color;
      });
    }

    if (options.markers && !options.markers.strokeColor) {
      options.markers.strokeColor = colors;
    }

    if (options.fill?.type === "gradient" && options.fill.gradient) {
      options.fill.gradient.gradientToColors = options.fill.gradient.gradientToColors || colors;
    }

    if (options.plotOptions?.treemap?.colorScale?.ranges) {
      const ranges = options.plotOptions.treemap.colorScale.ranges;
      if (ranges.length > 0 && !ranges[0].color) ranges[0].color = colors[0];
      if (ranges.length > 1 && !ranges[1].color) ranges[1].color = colors[1];
    }

    return options;
  }

  static rerenderAll() {
    CustomApexChart.instances.forEach(chart => chart.render());
  }
}

// ECharts Wrapper
class CustomEChart {
  static instances = [];

  constructor({ selector, options: getOptions = {}, theme = null, initOptions = {} }) {
    if (!selector) {
      console.warn("CustomEChart: 'selector' is required.");
      return;
    }

    this.selector = selector;
    this.getOptions = getOptions;
    this.theme = theme;
    this.initOptions = initOptions;
    this.chart = null;

    try {
      this.render();
      CustomEChart.instances.push(this);
    } catch (err) {
      console.error("CustomEChart: Initialization error", err);
    }
  }

  render() {
    try {
      this.element = this.selector instanceof HTMLElement ? this.selector : document.querySelector(this.selector);
      if (this.chart) this.chart.dispose();

      if (!this.element) {
        console.warn(`CustomEChart: No element found for selector '${this.selector}'.`);
        return;
      }

      const options = this.getOptions();
      this.chart = echarts.init(this.element, this.theme, this.initOptions);
      this.chart.setOption(options);

      window.addEventListener("resize", debounce(() => this.chart.resize(), 200));
    } catch (err) {
      console.error(`CustomEChart: Render error for '${this.selector}'`, err);
    }
  }

  static reSizeAll() {
    CustomEChart.instances.forEach(chart => {
      if (chart.element && chart.element.offsetParent !== null) {
        requestAnimationFrame(() => {
          chart.chart.on("finished", () => {
            requestAnimationFrame(() => chart.chart.resize());
          });
        });
      }
    });
  }

  static rerenderAll() {
    CustomEChart.instances.forEach(chart => chart.render());
  }
}

// Theme & Menu Observers
const themeObserver = new MutationObserver(() => {
  CustomApexChart.rerenderAll();
  CustomEChart.rerenderAll();
});
themeObserver.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["data-skin", "data-bs-theme"]
});

const menuObserver = new MutationObserver(() => {
  requestAnimationFrame(() => CustomEChart.reSizeAll());
});
menuObserver.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["data-sidenav-size"]
});

// Initialize on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  new App().init();
  new LayoutCustomizer().init();
  new Plugins().init();
});