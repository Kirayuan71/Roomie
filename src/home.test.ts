import {describe,it,expect} from 'vitest';
import {seed,migrateState,today,type State} from './data';
import {calendarEntries} from './HomeExtras';
describe('日历和留言数据升级',()=>{
 it('旧版数据升级保留已有账单和任务',()=>{const old=seed();const bills=old.bills;delete (old as Partial<State>).events;delete (old as Partial<State>).messages;const next=migrateState(old);expect(next.bills).toBe(bills);expect(next.events.length).toBeGreaterThan(0);expect(next.messages.length).toBeGreaterThan(0)});
 it('保留用户主动清空的安排和留言',()=>{const next=migrateState({...seed(),events:[],messages:[]});expect(next.events).toEqual([]);expect(next.messages).toEqual([])});
 it('生日逐年显示，普通提醒只在指定日期显示',()=>{const s=seed();s.tasks=[];s.events=[{id:'b',name:'生日',date:'2025-10-21',type:'室友生日',owner:'林小满',annual:true,done:false},{id:'c',name:'检查',date:'2025-10-21',type:'卫生检查',owner:'全体室友',annual:false,done:false}];expect(calendarEntries(s,'2026-10-21').map(e=>e.id)).toEqual(['b']);expect(calendarEntries(s,'2025-10-21')).toHaveLength(2)});
 it('清洁任务和完成状态来自值日表',()=>{const s=seed();const task=s.tasks[0];task.date=today();task.done=true;expect(calendarEntries(s,today()).find(e=>e.id===task.id)).toMatchObject({done:true,task:true,type:'清洁值日'})});
});
