import { HTMLManager } from "@jupyter-widgets/html-manager";
import { IModelOptions, IClassicComm } from "@jupyter-widgets/base";
import * as utils from "@jupyter-widgets/base";
import { IManagerState } from "@jupyter-widgets/base-manager";
export declare type WidgetModel = utils.DOMWidgetModel;
export declare type ModelBundle = {
    spec: {
        model_id: string;
    };
    state: IManagerState;
};
export declare class WidgetManager extends HTMLManager {
    private _known_models;
    private kernel_manager;
    private kernel;
    private ws;
    private _model_objs;
    protected bk_send?: (data: string | ArrayBuffer) => void;
    make_WebSocket(): {
        new (url: string, _protocols?: string | string[] | undefined): {
            binaryType: BinaryType;
            readonly bufferedAmount: number;
            readonly extensions: string;
            readonly protocol: string;
            readonly readyState: number;
            readonly CLOSED: number;
            readonly CLOSING: number;
            readonly CONNECTING: number;
            readonly OPEN: number;
            readonly url: string;
            close(code?: number | undefined, reason?: string | undefined): void;
            send(data: string | ArrayBufferLike | Blob | ArrayBufferView): void;
            onclose: ((this: WebSocket, ev: CloseEvent) => unknown) | null;
            onerror: ((this: WebSocket, ev: Event) => unknown) | null;
            onmessage: ((this: WebSocket, ev: MessageEvent) => unknown) | null;
            onopen: ((this: WebSocket, ev: Event) => unknown) | null;
            addEventListener(_type: string, _listener: EventListenerOrEventListenerObject, _options?: boolean | AddEventListenerOptions | undefined): void;
            removeEventListener(_type: string, _listener: EventListenerOrEventListenerObject, _options?: boolean | EventListenerOptions | undefined): void;
            dispatchEvent(_event: Event): boolean;
        };
        readonly CLOSED: number;
        readonly CLOSING: number;
        readonly CONNECTING: number;
        readonly OPEN: number;
    };
    bk_open(send_fn: (data: string | ArrayBuffer) => void): void;
    bk_recv(data: string | ArrayBuffer): void;
    private _comms;
    constructor(options: any);
    _attach_comm(comm: any, model: WidgetModel): void;
    render(bundle: ModelBundle, el: HTMLElement): Promise<void>;
    _create_comm(target_name: string, model_id: string, data?: any, metadata?: any, buffers?: ArrayBuffer[] | ArrayBufferView[]): Promise<IClassicComm>;
    _get_comm_info(): Promise<any>;
    new_model(options: IModelOptions, serialized_state?: any): Promise<WidgetModel>;
}
