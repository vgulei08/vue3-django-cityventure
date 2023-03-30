import * as api from './api';
import { dict, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions, compute } from '@fast-crud/fast-crud';
import { request } from '/@/utils/service';
import { dictionary } from '/@/utils/dictionary';
import { successMessage } from '/@/utils/message';
interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

export const createCrudOptions = function ({ crudExpose }: { crudExpose: CrudExpose }): CreateCrudOptionsTypes {
	const pageRequest = async (query: PageQuery) => {
		return await api.GetList(query);
	};
	const editRequest = async ({ form, row }: EditReq) => {
		form.id = row.id;
		return await api.UpdateObj(form);
	};
	const delRequest = async ({ row }: DelReq) => {
		return await api.DelObj(row.id);
	};
	const addRequest = async ({ form }: AddReq) => {
		return await api.AddObj(form);
	};

	/**
	 * 懒加载
	 * @param row
	 * @returns {Promise<unknown>}
	 */
	const loadContentMethod = (tree: any, treeNode: any, resolve: any) => {
		api.GetList({ pcode: tree.code }).then((res: any) => {
			resolve(res.data);
		});
	};

	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			rowHandle: {
				//固定右侧
				fixed: 'right',
				width: 200,
				buttons: {
					view: {
						show: false,
					},
					edit: {
						iconRight: 'Edit',
						type: 'text',
					},
					remove: {
						iconRight: 'Delete',
						type: 'text',
					},
				},
			},
			pagination: {
				show: false,
			},
			table: {
				rowKey: 'id',
				lazy: true,
				load: loadContentMethod,
				treeProps: { children: 'children', hasChildren: 'hasChild' },
			},
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
					column: {
						type: 'index',
						align: 'center',
						width: '70px',
						columnSetDisabled: true, //禁止在列设置中选择
					},
				},
				// pcode: {
				// 	title: '父级地区',
				// 	show: false,
				// 	search: {
				// 		show: true,
				// 	},
				// 	type: 'dict-tree',
				// 	form: {
				// 		component: {
				// 			showAllLevels: false, // 仅显示最后一级
				// 			props: {
				// 				elProps: {
				// 					clearable: true,
				// 					showAllLevels: false, // 仅显示最后一级
				// 					props: {
				// 						checkStrictly: true, // 可以不需要选到最后一级
				// 						emitPath: false,
				// 						clearable: true,
				// 					},
				// 				},
				// 			},
				// 		},
				// 	},
				// },
				name: {
					title: '名称',
					search: {
						show: true,
					},
					treeNode: true,
					width: 160,
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '名称必填项' },
						],
						component: {
							placeholder: '请输入名称',
						},
					},
				},
				code: {
					title: '地区编码',
					search: {
						show: true,
					},
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '地区编码必填项' },
						],
						component: {
							placeholder: '请输入地区编码',
						},
					},
				},
				pinyin: {
					title: '拼音',
					search: {
						disabled: true,
					},
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '拼音必填项' },
						],
						component: {
							placeholder: '请输入拼音',
						},
					},
				},
				level: {
					title: '地区层级',
					search: {
						disabled: true,
					},
					type: 'input',
					form: {
						disabled: false,
						rules: [
							// 表单校验规则
							{ required: true, message: '拼音必填项' },
						],
						component: {
							placeholder: '请输入拼音',
						},
					},
				},
				initials: {
					title: '首字母',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '首字母必填项' },
						],

						component: {
							placeholder: '请输入首字母',
						},
					},
				},
				enable: {
					title: '是否启用',
					search: {
						show: true,
					},
					width: 90,
					type: 'dict-radio',
					column: {
						component: {
							name: 'fs-dict-switch',
							activeText: '',
							inactiveText: '',
							style: '--el-switch-on-color: #409eff; --el-switch-off-color: #dcdfe6',
							onChange: compute((context) => {
								return () => {
									api.UpdateObj(context.row).then((res: APIResponseData) => {
										successMessage(res.msg as string);
									});
								};
							}),
						},
					},
					dict: dict({
						data: dictionary('button_status_bool'),
					}),
				},
			},
		},
	};
};
