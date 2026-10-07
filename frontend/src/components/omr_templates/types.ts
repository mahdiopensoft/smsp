export interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface BarcodeField {
  id: string;
  type: string;
  rect: Rect;
  value: string;
  format?: string;
  rotate?: number;
  displayValue?: boolean;
}

export interface QrCodeField {
  id: string;
  type: string;
  rect: Rect;
  value: string;
}

export interface BubbleOption {
  label: string;
  value: string;
  cx: number;
  cy: number;
  r: number;
}
