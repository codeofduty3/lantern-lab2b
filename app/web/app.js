(() => {
  "use strict";

  const isLocal =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost";
  const API_BASE =
    window.LANTERN_API_BASE || (isLocal ? "http://127.0.0.1:8000" : "/api");
  const DOCS_URL = isLocal ? "http://127.0.0.1:8000/docs" : "/docs";
  const validCategories = new Set([
    "comparative_leakage",
    "totals_counted",
    "cash_lines",
    "restated_copies",
    "unfunded_commitments",
    "custom_tags",
    "no_identified_holdings",
    "affiliate_split",
    "no_filed_total",
    "other",
  ]);

  const byId = (id) => document.getElementById(id);
  const money = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
  const compactMoney = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 2,
  });
  const integer = new Intl.NumberFormat("en-US");

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function formatMoney(value, compact = false) {
    if (value === null || value === undefined) return "n/a";
    return (compact ? compactMoney : money).format(value);
  }

  function formatPercent(value, signed = false) {
    if (value === null || value === undefined) return "n/a";
    const text = `${(value * 100).toFixed(1)}%`;
    return signed && value > 0 ? `+${text}` : text;
  }

  function formatCount(value) {
    return value === null || value === undefined ? "n/a" : integer.format(value);
  }

  function categoryLabel(value) {
    return value ? value.replaceAll("_", " ") : "n/a";
  }

  async function api(path) {
    const response = await fetch(`${API_BASE}${path}`, {
      headers: { Accept: "application/json" },
    });
    let body;
    try {
      body = await response.json();
    } catch {
      throw new Error(`The API returned ${response.status} without JSON.`);
    }
    if (!response.ok) {
      const detail = body.detail;
      throw new Error(
        typeof detail === "string"
          ? detail
          : detail?.message || `Request failed (${response.status}).`,
      );
    }
    return body;
  }

  function setActiveNav() {
    const page = document.body.dataset.nav;
    document.querySelectorAll("[data-nav-item]").forEach((link) => {
      if (link.dataset.navItem === page) {
        link.setAttribute("aria-current", "page");
      }
    });
  }

  function filingLink(adsh) {
    return `filing.html?adsh=${encodeURIComponent(adsh)}`;
  }

  function statusPill(admitted) {
    return admitted
      ? '<span class="pill yes">Admitted</span>'
      : '<span class="pill no">Excluded</span>';
  }

  async function fillCoverageBanner() {
    const coverage = await api("/coverage");
    document.querySelectorAll("[data-coverage-banner]").forEach((element) => {
      element.innerHTML = `
        <span class="coverage-badge">Coverage is not 100%</span>
        <p><strong>${formatCount(coverage.filings_admitted)} of ${formatCount(
          coverage.filings_attempted,
        )} filings</strong> and <strong>${formatMoney(
          coverage.filed_fv_admitted,
          true,
        )}</strong> of <strong>${formatMoney(
          coverage.filed_fv_attempted,
          true,
        )}</strong> filed fair value are represented.</p>
        <a href="excluded.html">See every excluded filing</a>
      `;
    });
    return coverage;
  }

  async function renderCoveragePage() {
    const coverage = await fillCoverageBanner();
    const grid = byId("coverage-stats");
    grid.innerHTML = `
      <article class="stat">
        <span class="stat-label">Filings admitted</span>
        <strong class="stat-value">${formatCount(coverage.filings_admitted)}</strong>
        <span class="coverage-badge">Coverage: ${formatPercent(
          coverage.share_of_filings,
        )} of filings</span>
      </article>
      <article class="stat">
        <span class="stat-label">Filings attempted</span>
        <strong class="stat-value">${formatCount(coverage.filings_attempted)}</strong>
        <span class="stat-coverage">${formatCount(
          coverage.filings_attempted - coverage.filings_admitted,
        )} remain excluded and visible</span>
      </article>
      <article class="stat">
        <span class="stat-label">Filed FV admitted</span>
        <strong class="stat-value">${formatMoney(
          coverage.filed_fv_admitted,
          true,
        )}</strong>
        <span class="coverage-badge">Coverage: ${formatPercent(
          coverage.share_of_dollars,
        )} of filed dollars</span>
      </article>
      <article class="stat">
        <span class="stat-label">No SOI rows</span>
        <strong class="stat-value">${formatCount(
          coverage.filings_without_soi_rows,
        )}</strong>
        <span class="stat-coverage">Reported separately from attempts</span>
      </article>
    `;

    const filings = (await api("/filings")).filings;
    const admitted = filings
      .filter((filing) => filing.admitted)
      .sort((a, b) => b.filed_fv - a.filed_fv);
    byId("top-filings").innerHTML = admitted
      .slice(0, 10)
      .map(
        (filing) => `
          <tr>
            <td><a class="filing-name" href="${filingLink(
              filing.adsh,
            )}">${escapeHtml(filing.name)}</a><div class="small muted mono">${escapeHtml(
              filing.adsh,
            )}</div></td>
            <td class="num">${formatMoney(filing.holdings_fv)}</td>
            <td class="num">${formatMoney(filing.filed_fv)}</td>
            <td class="num">${formatPercent(filing.gap_pct, true)}</td>
          </tr>`,
      )
      .join("");
  }

  async function renderFilingsPage() {
    await fillCoverageBanner();
    const response = await api("/filings");
    const filings = response.filings;
    const filter = byId("filing-filter");
    const status = byId("status-filter");
    const count = byId("filing-count");

    const draw = () => {
      const query = filter.value.trim().toLowerCase();
      const wanted = status.value;
      const visible = filings.filter((filing) => {
        const matchesText = [filing.name, filing.adsh, filing.triage_category]
          .join(" ")
          .toLowerCase()
          .includes(query);
        const matchesStatus =
          wanted === "all" ||
          (wanted === "admitted" && filing.admitted) ||
          (wanted === "excluded" && !filing.admitted);
        return matchesText && matchesStatus;
      });
      count.textContent = `${formatCount(visible.length)} of ${formatCount(
        filings.length,
      )} attempted filings`;
      byId("filings-body").innerHTML = visible
        .map(
          (filing) => `
            <tr>
              <td><a class="filing-name" href="${filingLink(
                filing.adsh,
              )}">${escapeHtml(filing.name)}</a><div class="small muted mono">${escapeHtml(
                filing.adsh,
              )}</div></td>
              <td>${escapeHtml(filing.form)}<div class="muted small">${escapeHtml(
                filing.period,
              )}</div></td>
              <td class="num">${formatMoney(filing.holdings_fv)}</td>
              <td class="num">${formatMoney(filing.filed_fv)}</td>
              <td class="num">${formatPercent(filing.gap_pct, true)}</td>
              <td>${statusPill(filing.admitted)}</td>
              <td>${
                filing.admitted
                  ? '<span class="muted">n/a</span>'
                  : `<a href="excluded.html?category=${encodeURIComponent(
                      filing.triage_category,
                    )}">${escapeHtml(categoryLabel(filing.triage_category))}</a>`
              }</td>
            </tr>`,
        )
        .join("");
      if (!visible.length) {
        byId("filings-body").innerHTML =
          '<tr><td colspan="7" class="empty">No filings match these filters.</td></tr>';
      }
    };
    filter.addEventListener("input", draw);
    status.addEventListener("change", draw);
    draw();
  }

  function holdingRow(holding) {
    const sources = String(holding.source_rows || "").split(";").join(", ");
    return `
      <tr>
        <td><span class="filing-name">${escapeHtml(
          holding.identifier,
        )}</span><div class="small muted">${
          holding.security_class
            ? escapeHtml(holding.security_class)
            : "unclassified"
        } · ${escapeHtml(holding.affiliation_category || "unspecified")}</div></td>
        <td>${escapeHtml(holding.investment_type || "n/a")}</td>
        <td class="num">${formatMoney(holding.fair_value)}</td>
        <td class="num">${formatMoney(holding.cost)}</td>
        <td class="num">${formatMoney(holding.principal)}</td>
        <td class="num">${formatCount(holding.n_rows)}</td>
        <td class="mono">${escapeHtml(sources)}</td>
      </tr>`;
  }

  async function renderFilingPage() {
    const adsh = new URLSearchParams(window.location.search).get("adsh");
    if (!adsh) {
      byId("filing-content").innerHTML =
        '<div class="error">Choose a filing from the <a href="filings.html">filings page</a>.</div>';
      return;
    }
    const filing = await api(`/filings/${encodeURIComponent(adsh)}`);
    document.title = `${filing.name} · Project LANTERN`;
    byId("filing-name").textContent = filing.name;
    byId("filing-eyebrow").textContent = `${filing.form} · ${filing.period} · ${filing.adsh}`;
    const edgar = byId("edgar-link");
    edgar.href = filing.edgar_url;
    edgar.hidden = false;
    byId("filing-status").innerHTML = statusPill(filing.admitted);

    if (!filing.admitted) {
      byId("filing-content").innerHTML = `
        <div class="callout">
          <strong>This filing was attempted but excluded from the holdings panel.</strong>
          <p>Reported gap: ${formatPercent(filing.gap_pct, true)}. Its category is
          ${escapeHtml(categoryLabel(filing.triage_category))}.
          <a href="excluded.html">Review the evidence for every exclusion.</a></p>
        </div>`;
      return;
    }

    const holdingsDocument = await api(
      `/filings/${encodeURIComponent(adsh)}/holdings`,
    );
    byId("holding-sum").textContent = formatMoney(holdingsDocument.holdings_fv);
    byId("filed-total").textContent = formatMoney(filing.filed_fv);
    byId("filing-gap").textContent = formatPercent(filing.gap_pct, true);
    byId("holding-count").textContent = formatCount(
      holdingsDocument.holdings.length,
    );
    byId("holding-coverage").textContent =
      `This filing's ${formatMoney(holdingsDocument.holdings_fv, true)} admits ` +
      `100% of its own reported total; release-wide dollar coverage is ${formatPercent(
        (await api("/coverage")).share_of_dollars,
      )}.`;

    const body = byId("holdings-body");
    const search = byId("holding-search");
    const draw = () => {
      const query = search.value.trim().toLowerCase();
      const visible = holdingsDocument.holdings.filter((holding) =>
        [
          holding.identifier,
          holding.investment_type,
          holding.industry,
          holding.security_class,
          holding.source_rows,
        ]
          .join(" ")
          .toLowerCase()
          .includes(query),
      );
      body.innerHTML = visible.map(holdingRow).join("");
      byId("holding-match").textContent = `${formatCount(
        visible.length,
      )} holdings shown`;
      if (!visible.length) {
        body.innerHTML =
          '<tr><td colspan="7" class="empty">No holdings match this search.</td></tr>';
      }
    };
    search.addEventListener("input", draw);
    draw();
  }

  async function renderExcludedPage() {
    await fillCoverageBanner();
    const triage = (await api("/triage")).triage;
    const category = new URLSearchParams(window.location.search).get("category");
    const filter = byId("triage-filter");
    filter.value = category && validCategories.has(category) ? category : "all";
    const draw = () => {
      const visible = triage.filter(
        (item) => filter.value === "all" || item.triage_category === filter.value,
      );
      byId("triage-count").textContent = `${formatCount(
        visible.length,
      )} excluded filings shown`;
      byId("triage-list").innerHTML = visible
        .map(
          (item) => `
            <article class="triage-card">
              <header>
                <div>
                  <span class="eyebrow">${escapeHtml(
                    categoryLabel(item.triage_category),
                  )}</span>
                  <h2>${escapeHtml(item.name)}</h2>
                  <div class="small muted mono">${escapeHtml(item.adsh)} · ${escapeHtml(
                    item.form,
                  )} · ${escapeHtml(item.period)}</div>
                </div>
                <strong class="num">${formatPercent(item.gap_pct, true)}</strong>
              </header>
              <p><strong>Evidence:</strong> ${escapeHtml(item.evidence)}</p>
              <p><strong>Example:</strong> <span class="mono">${escapeHtml(
                item.example,
              )}</span></p>
              <p><strong>Why it remains excluded:</strong> ${escapeHtml(item.fix)}</p>
              <a href="${escapeHtml(item.edgar_url)}" rel="noreferrer">Open the SEC filing</a>
            </article>`,
        )
        .join("");
      if (!visible.length) {
        byId("triage-list").innerHTML =
          '<div class="empty">No exclusions use this category.</div>';
      }
    };
    filter.addEventListener("change", draw);
    draw();
  }

  async function renderMethodPage() {
    await fillCoverageBanner();
    const rules = (await api("/cleaning-rules")).rules;
    byId("rule-list").innerHTML = rules
      .map(
        (rule, index) => `
          <article class="rule">
            <div class="rule-head">
              <div>
                <span class="eyebrow">Step ${index + 1}</span>
                <h2 class="mono">${escapeHtml(rule.rule)}</h2>
              </div>
              <span class="pill neutral">${formatCount(
                rule.rows_affected,
              )} rows affected</span>
            </div>
            <p>${escapeHtml(rule.motivation)}</p>
            <dl class="rule-grid">
              <div><dt>Structural artifact</dt><dd>${escapeHtml(
                rule.artifact,
              )}</dd></div>
              <div><dt>Example</dt><dd><span class="mono">${escapeHtml(
                rule.example_adsh,
              )} / SOI ${escapeHtml(rule.example_soi_row)}</span></dd></div>
              <div><dt>Coverage in log</dt><dd>${formatPercent(
                rule.coverage_before,
              )} before → ${formatPercent(rule.coverage_after)} after</dd></div>
            </dl>
          </article>`,
      )
      .join("");
  }

  async function start() {
    setActiveNav();
    document.querySelectorAll('a[href="/docs"]').forEach((link) => {
      link.href = DOCS_URL;
    });
    const page = document.body.dataset.page;
    try {
      if (page === "coverage") await renderCoveragePage();
      if (page === "filings") await renderFilingsPage();
      if (page === "filing") await renderFilingPage();
      if (page === "excluded") await renderExcludedPage();
      if (page === "method") await renderMethodPage();
    } catch (error) {
      const target =
        byId("page-error") ||
        byId("filing-content") ||
        byId("triage-list") ||
        byId("rule-list");
      if (target) {
        target.innerHTML = `<div class="error">${escapeHtml(
          error.message,
        )}</div>`;
      }
      console.error(error);
    }
  }

  start();
})();
