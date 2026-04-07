import { LitElement, html, css } from "lit";
import { customElement, state } from "lit/decorators.js";
import type { GraphResponse, SweepResponse } from "../lib/api";
import { generateGraph, percolateGraph, runSweep } from "../lib/api";
import "./graph-canvas";
import "./sweep-chart";

@customElement("phase-app")
export class PhaseApp extends LitElement {
  static styles = css`
    :host { display: block; height: 100vh; background: var(--bg-primary); color: var(--text-primary); }
    .top-bar {
      display: flex; align-items: center; gap: 1rem;
      padding: 0.5rem 1rem; background: var(--bg-secondary);
      border-bottom: 1px solid var(--border); height: 48px;
    }
    .top-bar h1 { font-size: 0.95rem; font-weight: 700; color: var(--accent); white-space: nowrap; }
    .top-bar h1 span { color: var(--text-primary); margin-left: 0.4rem; }

    .main { display: grid; grid-template-columns: 1fr 1fr; height: calc(100vh - 48px); }
    .left, .right { display: flex; flex-direction: column; overflow: hidden; }
    .left { border-right: 1px solid var(--border); }

    .controls {
      display: flex; flex-wrap: wrap; gap: 0.5rem; padding: 0.6rem;
      background: var(--bg-secondary); border-bottom: 1px solid var(--border);
      align-items: end; font-size: 0.78rem;
    }
    .ctrl-group { display: flex; flex-direction: column; gap: 0.15rem; }
    .ctrl-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: var(--text-muted); }
    select, input[type="number"] {
      padding: 0.3rem 0.4rem; border: 1px solid var(--border); border-radius: var(--radius-sm);
      background: var(--bg-input); color: var(--text-primary); font-size: 0.78rem; outline: none; width: 80px;
    }
    input[type="range"] { width: 100px; accent-color: var(--accent); }
    select:focus, input:focus { border-color: var(--accent); }

    .btn {
      padding: 0.35rem 0.7rem; border: none; border-radius: var(--radius-sm);
      font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: background 0.15s;
    }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-primary { background: var(--accent); color: white; }
    .btn-primary:hover:not(:disabled) { background: var(--accent-hover); }
    .btn-secondary { background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border); }

    .info-bar {
      display: flex; gap: 1rem; padding: 0.4rem 0.6rem;
      background: var(--bg-secondary); border-bottom: 1px solid var(--border);
      font-size: 0.72rem; color: var(--text-muted);
    }
    .info-bar .tag {
      padding: 0.15rem 0.4rem; border-radius: var(--radius-sm);
      font-weight: 600; font-size: 0.68rem;
    }
    .tag-ok { background: rgba(34,197,94,0.15); color: var(--success); }
    .tag-no { background: rgba(239,68,68,0.15); color: var(--danger); }

    .canvas-wrap { flex: 1; position: relative; }
    .chart-wrap { flex: 1; padding: 0.75rem; overflow-y: auto; }

    .chart-header { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 0.4rem; }
    .sweep-controls {
      display: flex; flex-wrap: wrap; gap: 0.5rem; padding: 0.6rem;
      background: var(--bg-secondary); border-bottom: 1px solid var(--border);
      align-items: end; font-size: 0.78rem;
    }

    @media (max-width: 800px) {
      .main { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; }
      .left { border-right: none; border-bottom: 1px solid var(--border); }
    }
  `;

  @state() model = "binomial";
  @state() n = 50;
  @state() param = 0.1;
  @state() seed = 42;
  @state() graphData: GraphResponse | null = null;

  @state() percType = "node";
  @state() percQ = 1.0;
  @state() percData: GraphResponse | null = null;

  @state() sweepData: SweepResponse | null = null;
  @state() sweeping = false;
  @state() sweepTrials = 10;
  @state() sweepSteps = 20;

  connectedCallback() {
    super.connectedCallback();
    this._generate();
  }

  private async _generate() {
    try {
      this.graphData = await generateGraph(this.model, this.n, this.param, this.seed);
      this.percData = null;
      this.percQ = 1.0;
    } catch {}
  }

  private async _percolate() {
    try {
      this.percData = await percolateGraph(this.model, this.n, this.param, this.seed, this.percType, this.percQ);
    } catch {}
  }

  private async _sweep() {
    this.sweeping = true;
    try {
      const paramMax = this.model === "geometric" ? 1.0 : this.model === "binomial" ? 0.5 : 1.0;
      this.sweepData = await runSweep({
        model: this.model,
        n: this.n,
        param_min: 0,
        param_max: paramMax,
        param_steps: this.sweepSteps,
        trials: this.sweepTrials,
        seed: this.seed,
      });
    } catch {}
    this.sweeping = false;
  }

  private _onParamInput(e: Event) {
    this.param = +(e.target as HTMLInputElement).value;
    this._generate();
  }

  private _onQInput(e: Event) {
    this.percQ = +(e.target as HTMLInputElement).value;
    this._percolate();
  }

  render() {
    const display = this.percData ?? this.graphData;
    return html`
      <div class="top-bar">
        <h1>Phase Transitions<span>in Random Graphs</span></h1>
      </div>
      <div class="main">
        <div class="left">
          <div class="controls">
            <div class="ctrl-group">
              <span class="ctrl-label">Model</span>
              <select .value=${this.model} @change=${(e: Event) => { this.model = (e.target as HTMLSelectElement).value; this._generate(); }}>
                <option value="binomial">Binomial G(n,p)</option>
                <option value="geometric">Geometric RGG(n,r)</option>
                <option value="grid">Grid n×n</option>
              </select>
            </div>
            <div class="ctrl-group">
              <span class="ctrl-label">N</span>
              <input type="number" min="4" max="500" .value=${String(this.n)}
                @change=${(e: Event) => { this.n = +(e.target as HTMLInputElement).value; this._generate(); }} />
            </div>
            <div class="ctrl-group">
              <span class="ctrl-label">${this.model === "geometric" ? "Radius (r)" : this.model === "binomial" ? "Prob (p)" : "Side"}</span>
              <input type="range" min="0" max=${this.model === "geometric" ? "1.0" : "0.5"} step="0.01"
                .value=${String(this.param)} @input=${this._onParamInput} />
              <span style="font-family:var(--font-mono);font-size:0.72rem">${this.param.toFixed(2)}</span>
            </div>
            <div class="ctrl-group">
              <span class="ctrl-label">Seed</span>
              <input type="number" .value=${String(this.seed)}
                @change=${(e: Event) => { this.seed = +(e.target as HTMLInputElement).value; this._generate(); }} />
            </div>
            <button class="btn btn-secondary" @click=${() => { this.seed = Math.floor(Math.random() * 100000); this._generate(); }}>Random</button>
          </div>
          <div class="controls">
            <div class="ctrl-group">
              <span class="ctrl-label">Percolation</span>
              <select .value=${this.percType} @change=${(e: Event) => { this.percType = (e.target as HTMLSelectElement).value; if (this.percQ < 1) this._percolate(); }}>
                <option value="node">Node</option>
                <option value="edge">Edge</option>
                <option value="composed">Composed</option>
              </select>
            </div>
            <div class="ctrl-group">
              <span class="ctrl-label">q (keep prob)</span>
              <input type="range" min="0" max="1" step="0.02" .value=${String(this.percQ)} @input=${this._onQInput} />
              <span style="font-family:var(--font-mono);font-size:0.72rem">${this.percQ.toFixed(2)}</span>
            </div>
          </div>
          ${display ? html`
            <div class="info-bar">
              <span>Nodes: <b>${display.n}</b></span>
              <span>Edges: <b>${display.edges.length}</b></span>
              <span>Components: <b>${display.n_components}</b></span>
              <span class="tag ${display.connected ? "tag-ok" : "tag-no"}">${display.connected ? "Connected" : "Disconnected"}</span>
              <span class="tag ${display.is_complex ? "tag-ok" : "tag-no"}">${display.is_complex ? "Complex" : "Not complex"}</span>
            </div>
          ` : ""}
          <div class="canvas-wrap">
            <graph-canvas .data=${display}></graph-canvas>
          </div>
        </div>
        <div class="right">
          <div class="sweep-controls">
            <div class="ctrl-group">
              <span class="ctrl-label">Trials</span>
              <input type="number" min="1" max="100" .value=${String(this.sweepTrials)}
                @change=${(e: Event) => { this.sweepTrials = +(e.target as HTMLInputElement).value; }} />
            </div>
            <div class="ctrl-group">
              <span class="ctrl-label">Steps</span>
              <input type="number" min="5" max="50" .value=${String(this.sweepSteps)}
                @change=${(e: Event) => { this.sweepSteps = +(e.target as HTMLInputElement).value; }} />
            </div>
            <button class="btn btn-primary" @click=${this._sweep} ?disabled=${this.sweeping}>
              ${this.sweeping ? "Running..." : "Run Sweep"}
            </button>
          </div>
          <div class="chart-wrap">
            ${this.sweepData
              ? html`
                <div class="chart-header">Phase Transition Curves (${this.sweepData.model}, n=${this.sweepData.n})</div>
                <sweep-chart .data=${this.sweepData}></sweep-chart>
              `
              : html`<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);font-size:0.85rem;">Click <b style="margin:0 0.3rem">Run Sweep</b> to generate phase transition curves</div>`}
          </div>
        </div>
      </div>
    `;
  }
}
