const BASE = import.meta.env.VITE_API_URL ?? "";

export interface NodeData {
  id: number;
  x: number;
  y: number;
  component: number;
}

export interface GraphResponse {
  nodes: NodeData[];
  edges: [number, number][];
  n: number;
  connected: boolean;
  is_complex: boolean;
  n_components: number;
}

export interface SweepPoint {
  param: number;
  p_connected: number;
  p_complex: number;
  p_both: number;
}

export interface SweepResponse {
  model: string;
  n: number;
  param_name: string;
  trials: number;
  points: SweepPoint[];
}

async function post<T>(url: string, body: unknown): Promise<T> {
  const r = await fetch(`${BASE}${url}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export const generateGraph = (model: string, n: number, param: number, seed?: number) =>
  post<GraphResponse>("/api/generate", { model, n, param, seed });

export const percolateGraph = (
  model: string, n: number, param: number, seed: number | undefined,
  percolation_type: string, q: number,
) => post<GraphResponse>("/api/percolate", { model, n, param, seed, percolation_type, q });

export const runSweep = (params: {
  model: string;
  n: number;
  param_min: number;
  param_max: number;
  param_steps: number;
  trials: number;
  percolation_type?: string;
  base_param?: number;
  seed?: number;
}) => post<SweepResponse>("/api/sweep", params);
