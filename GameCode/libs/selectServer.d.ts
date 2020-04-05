declare function dnsSeverSelectorInit(protocol:string,subDnsCount:number,subDns:string,mainDns:string,port:number,defautAddress:string):void
declare function selectDnsSever(cb:any):void
declare function getDnsSever():string
declare function getSelectDns():string
declare function getDefaultDns(port:number):string
declare function getNetworkPort(protocol:string):number