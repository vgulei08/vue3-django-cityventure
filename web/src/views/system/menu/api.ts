import { request } from '/@/utils/service';
import { UserPageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';

export const apiPrefix = '/api/system/menu/';
export function GetList(query: UserPageQuery) {
	return request({
		url: apiPrefix,
		method: 'get',
		params: query,
	});
}

export function GetObj(id: InfoReq) {
	return request({
		url: apiPrefix + id + '/',
		method: 'get',
	});
}

export function AddObj(obj: AddReq) {
	return request({
		url: apiPrefix,
		method: 'post',
		data: obj,
	});
}

export function UpdateObj(obj: EditReq) {
	return request({
		url: apiPrefix + obj.id + '/',
		method: 'put',
		data: obj,
	});
}

export function DelObj(obj: DelReq) {
	return request({
		url: apiPrefix + obj.id + '/',
		method: 'delete',
	});
}

export function GetAllMenu(query: UserPageQuery) {
	return request({
		url: apiPrefix + 'get_all_menu/',
		method: 'get',
		params: query,
	});
}

export function lazyLoadMenu(query: UserPageQuery) {
	return request({
		url: apiPrefix,
		method: 'get',
		params: query,
	});
}

export function dragMenu(obj: AddReq) {
	return request({
		url: apiPrefix + 'drag_menu/',
		method: 'post',
		data: obj,
	});
}
