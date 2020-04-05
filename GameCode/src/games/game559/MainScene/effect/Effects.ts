/**
 * Created by Administrator on 2018/5/4.
 */
module G559 {
    export namespace rf {
        interface i_Effects extends Vuet {
            ptMap;
        }
        export class Effects extends G560.fl.Effects {
            constructor() {
                super();
            }
            static create(component, params) {
                let base = super.create(component, params);
                let vuetparams: any = base._config;
                vuetparams.params.ptMap = {};
                return <i_Effects>new Vuet(vuetparams);
            }
        }
    }

}