import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";
import type { GraphResponse } from "../lib/api";

const COMPONENT_COLORS = [
  "#06b6d4", "#d946ef", "#22c55e", "#f97316", "#ec4899",
  "#14b8a6", "#a855f7", "#eab308", "#f43f5e", "#3b82f6",
];

@customElement("graph-canvas")
export class GraphCanvas extends LitElement {
  static styles = css`
    :host { display: block; width: 100%; height: 100%; }
    canvas { width: 100%; height: 100%; display: block; }
  `;

  @property({ type: Object }) data: GraphResponse | null = null;

  private _canvas?: HTMLCanvasElement;
  private _ro?: ResizeObserver;

  firstUpdated() {
    this._canvas = this.shadowRoot!.querySelector("canvas")!;
    this._ro = new ResizeObserver(() => this._draw());
    this._ro.observe(this._canvas);
    this._draw();
  }

  updated() {
    this._draw();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this._ro?.disconnect();
  }

  private _draw() {
    const canvas = this._canvas;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.fillStyle = "#0a0a15";
    ctx.fillRect(0, 0, w, h);

    const data = this.data;
    if (!data || data.nodes.length === 0) {
      ctx.fillStyle = "#64748b";
      ctx.font = "14px system-ui";
      ctx.textAlign = "center";
      ctx.fillText("No graph data", w / 2, h / 2);
      return;
    }

    const pad = 30;
    const nodes = data.nodes;
    const nodeMap = new Map(nodes.map((n) => [n.id, n]));

    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const n of nodes) {
      if (n.x < minX) minX = n.x;
      if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.y > maxY) maxY = n.y;
    }
    const rangeX = maxX - minX || 1;
    const rangeY = maxY - minY || 1;
    const sx = (x: number) => pad + ((x - minX) / rangeX) * (w - 2 * pad);
    const sy = (y: number) => pad + ((y - minY) / rangeY) * (h - 2 * pad);

    // Edges
    ctx.strokeStyle = "#2a2a40";
    ctx.lineWidth = 0.8;
    for (const [u, v] of data.edges) {
      const nu = nodeMap.get(u);
      const nv = nodeMap.get(v);
      if (!nu || !nv) continue;
      ctx.beginPath();
      ctx.moveTo(sx(nu.x), sy(nu.y));
      ctx.lineTo(sx(nv.x), sy(nv.y));
      ctx.stroke();
    }

    // Nodes
    const r = data.n > 200 ? 2 : data.n > 100 ? 3 : data.n > 50 ? 4 : 5;
    for (const n of nodes) {
      const color = n.component >= 0
        ? COMPONENT_COLORS[n.component % COMPONENT_COLORS.length]
        : "#64748b";
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(sx(n.x), sy(n.y), r, 0, Math.PI * 2);
      ctx.fill();
    }

    // Legend
    const ly = h - 12;
    ctx.font = "10px system-ui";
    ctx.textAlign = "left";
    const nComp = data.n_components;
    const shown = Math.min(nComp, 5);
    for (let i = 0; i < shown; i++) {
      const lx = pad + i * 70;
      ctx.fillStyle = COMPONENT_COLORS[i % COMPONENT_COLORS.length];
      ctx.beginPath();
      ctx.arc(lx, ly, 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#64748b";
      ctx.fillText(`C${i}`, lx + 6, ly + 3);
    }
    if (nComp > shown) {
      ctx.fillStyle = "#64748b";
      ctx.fillText(`+${nComp - shown} more`, pad + shown * 70, ly + 3);
    }
  }

  render() {
    return html`<canvas></canvas>`;
  }
}
