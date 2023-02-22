import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { directive } from '/@/utils/directive';
import { i18n } from '/@/i18n/index';
import other from '/@/utils/other';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';
import mitt from 'mitt';
import VueGridLayout from 'vue-grid-layout';
import piniaPersist from 'pinia-plugin-persist';
// @ts-ignore
import fastCrud from './settings.ts';
import pinia from './stores';
import permission from '/@/plugin/permission/index';
import eIconPicker, { iconList } from 'e-icon-picker';
import 'e-icon-picker/icon/default-icon/symbol.js'; //基本彩色图标库
import 'e-icon-picker/index.css'; // 基本样式，包含基本图标
import 'font-awesome/css/font-awesome.min.css';
import elementPlus from 'e-icon-picker/icon/ele/element-plus.js'; //element-plus的图标
import fontAwesome470 from 'e-icon-picker/icon/fontawesome/font-awesome.v4.7.0.js'; //fontAwesome470的图标
import eIconList from 'e-icon-picker/icon/default-icon/eIconList.js';
import { analyzingIconForIconfont } from 'e-icon-picker'; //引入解析json的函数
import iconfont from '/@/assets/iconfont/iconfont.json'; //引入json文件
import '/@/assets/iconfont/iconfont.css'; //引入css
let forIconfont = analyzingIconForIconfont(iconfont); //解析class
iconList.addIcon(forIconfont.list); // 添加iconfont dvadmin3的icon
iconList.addIcon(elementPlus); // 添加element plus的图标
iconList.addIcon(fontAwesome470); // 添加fontAwesome 470版本的图标

let app = createApp(App);

app.use(eIconPicker, {
	addIconList: eIconList, //全局添加图标
	removeIconList: [], //全局删除图标
	zIndex: 3100, //选择器弹层的最低层,全局配置
});

pinia.use(piniaPersist);
directive(app);
other.elSvg(app);

app.use(permission);
app.use(pinia).use(router).use(ElementPlus, { i18n: i18n.global.t }).use(i18n).use(VueGridLayout).use(fastCrud).mount('#app');

app.config.globalProperties.mittBus = mitt();
