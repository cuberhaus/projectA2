import { LitElement, html, svg, css } from "lit";
import { customElement, property } from "lit/decorators.js";
import type { SweepResponse } from "../lib/api";
import { scaleLinear } from "d3-scale";
import { line as d3Line } from "d3-shape";

const CURVES = [
  { key: "p_connected" as const, label: "P(connected)", color: "#3b82f6" },
  { key: "p_complex" as const, label: "P(complex)", color: "#f97316" },
  { key: "p_both" as const, label: "P(both)", color: "#22c55e" },
];

@customElement("sweep-chart")
export class SweepChart extends LitElement {
  static styles = css`
    :host { display: block; }
    svg { width: 100%; display: block; }
    .legend { display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.72rem; color: var(--text-muted); }
    .legend-item { display: flex; align-items: center; gap: 0.3rem; }
    .legend-dot { width: 10px; height: 3px; border-radius: 2px; display: inline-block; }
  `;

  @property({ type: Object }) data: SweepResponse | null = null;

  render() {
    if (!this.data || this.data.points.length < 2) {
      return html`<div style="color:var(--text-muted);font-size:0.82rem;">No sweep data</div>`;
    }

    const d = this.data;
    const W = 500, H = 280;
    const margin = { top: 20, right: 20, bottom: 35, left: 45 };
    const iw = W - margin.left - margin.right;
    const ih = H - margin.top - margin.bottom;

    const xScale = scaleLinear()
      .domain([d.points[0].param, d.points[d.points.length - 1].param])
      .range([0, iw]);

    const yScale = scaleLinear().domain([0, 1]).range([ih, 0]);

    const xTicks = xScale.ticks(6);
    const yTicks = [0, 0.25, 0.5, 0.75, 1.0];

    const paths = CURVES.map((c) => {
      const gen = d3Line<(typeof d.points)[0]>()
        .x((p) => xScale(p.param))
        .y((p) => yScale(p[c.key]));
      return { ...c, d: gen(d.points) ?? "" };
    });

    return html`
      <svg viewBox="0 0 ${W} ${H}">
        ${svg`<g transform="translate(${margin.left},${margin.top})">
          ${yTicks.map(
            (t) => svg`
              <line x1="0" x2="${iw}" y1="${yScale(t)}" y2="${yScale(t)}" stroke="#1a1a2e" stroke-width="1" />
              <text x="-6" y="${yScale(t) + 3}" fill="#64748b" font-size="9" text-anchor="end">${t}</text>
            `
          )}
          ${xTicks.map(
            (t) => svg`
              <line x1="${xScale(t)}" x2="${xScale(t)}" y1="0" y2="${ih}" stroke="#1a1a2e" stroke-width="1" />
              <text x="${xScale(t)}" y="${ih + 14}" fill="#64748b" font-size="9" text-anchor="middle">${t.toFixed(2)}</text>
            `
          )}
          ${paths.map(
            (p) => svg`<path d="${p.d}" fill="none" stroke="${p.color}" stroke-width="2" />`
          )}
          ${CURVES.flatMap((c) =>
            d.points.map(
              (pt) => svg`<circle cx="${xScale(pt.param)}" cy="${yScale(pt[c.key])}" r="2.5" fill="${c.color}" />`
            )
          )}
          <text x="${iw / 2}" y="${ih + 30}" fill="#64748b" font-size="10" text-anchor="middle">${d.param_name}</text>
          <text x="-30" y="${ih / 2}" fill="#64748b" font-size="10" text-anchor="middle" transform="rotate(-90,-30,${ih / 2})">Probability</text>
        </g>`}
      </svg>
      <div class="legend">
        ${CURVES.map(
          (c) => html`<span class="legend-item"><span class="legend-dot" style="background:${c.color}"></span> ${c.label}</span>`
        )}
      </div>
    `;
  }
}
