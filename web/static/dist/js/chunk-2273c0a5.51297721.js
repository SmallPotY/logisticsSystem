(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2273c0a5"],{5346:function(t,e,a){"use strict";a.d(e,"a",function(){return o}),a.d(e,"b",function(){return r});var n=a("66df"),o=function(t){return n["a"].request({url:"/reqExpressData",method:"post",data:t})},r=function(t){return n["a"].request({url:"/home",method:"post",data:t})}},fc98:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("Card",{attrs:{bordered:!1}},[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("快递信息跟踪")]),a("Form",{ref:"formInline",attrs:{model:t.form,inline:""}},[a("Form-Item",{attrs:{label:"日期选择:","label-width":80}},[a("DatePicker",{staticStyle:{width:"260px"},attrs:{type:"datetimerange",format:"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期范围"},on:{"on-change":function(e){t.form.dateRange=e}},model:{value:t.form.dateRange,callback:function(e){t.$set(t.form,"dateRange",e)},expression:"form.dateRange"}})],1),a("Form-Item",{attrs:{label:"承运商筛选:","label-width":80}},[a("i-select",{staticStyle:{width:"260px"},attrs:{multiple:""},model:{value:t.form.company,callback:function(e){t.$set(t.form,"company",e)},expression:"form.company"}},t._l(t.company,function(e){return a("i-option",{key:e.index,attrs:{value:e.value}},[t._v(t._s(e.label))])}))],1),a("Form-Item",{attrs:{label:"模糊搜索:","label-width":80}},[a("i-input",{staticStyle:{width:"200px"},attrs:{placeholder:"请输入..."},model:{value:t.form.wordKey,callback:function(e){t.$set(t.form,"wordKey",e)},expression:"form.wordKey"}})],1),a("i-button",{attrs:{type:"primary",shape:"circle",icon:"ios-search"},on:{click:t.handleSearch}},[t._v("搜索")])],1),a("Table",{attrs:{border:"",columns:t.columns,data:t.data},scopedSlots:t._u([{key:"name",fn:function(e){var n=e.row;return[a("strong",[t._v(t._s(n.name))])]}},{key:"action",fn:function(e){e.row;var n=e.index;return[a("Button",{staticStyle:{"margin-right":"5px"},attrs:{type:"primary",size:"small"},on:{click:function(e){t.show(n)}}},[t._v("View")]),a("Button",{attrs:{type:"error",size:"small"},on:{click:function(e){t.remove(n)}}},[t._v("Delete")])]}}])}),a("Page",{attrs:{total:t.page.total,current:t.page.current,"show-elevator":"","show-total":""},on:{"on-change":t.pageChange}})],1)},o=[],r=(a("7f7f"),a("cadf"),a("551c"),a("097d"),a("5346")),s={name:"expressInfo_page",data:function(){return{page:{current:1,total:1,size:40},self:this,company:[{value:"yto",label:"圆通"},{value:"zto",label:"中通"}],form:{dateRange:[],company:[],wordKey:""},columns:[{key:"updated_time",title:"数据更新时间"},{key:"order_time",title:"订单日期"},{key:"express_no",title:"快递单号"},{key:"express_company",title:"快递公司"},{key:"express_status",title:"快递状态"},{key:"latest_content",title:"当前节点"},{key:"latest_time",title:"节点时间"},{key:"to_address",title:"目的地"},{key:"identification",title:"订单来源"}],data:[]}},methods:{pageChange:function(t){this.page.current=t,this.handleSearch()},handleSearch:function(){var t=this,e={page_current:this.page.current,page_size:this.page.size,dateRang:this.form.dateRange,company:this.form.company,wordKey:this.form.wordKey};Object(r["a"])(e).then(function(e){t.data=e.data.data.tableData,t.page=e.data.data.page})},show:function(t){this.$Modal.info({title:"User Info",content:"Name：".concat(this.data[t].name,"<br>Age：").concat(this.data[t].age,"<br>Address：").concat(this.data[t].address)})},remove:function(t){this.data.splice(t,1)}}},i=s,l=a("2877"),c=Object(l["a"])(i,n,o,!1,null,null,null);c.options.__file="expressInfo.vue";e["default"]=c.exports}}]);