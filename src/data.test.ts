import {describe,it,expect} from 'vitest';
import {seed,balances,transfers,parseBill,people} from './data';
describe('跨模块账本计算',()=>{
it('非均摊参与者不负担支出，净额守恒',()=>{const bill={...seed().bills[0],amount:120,payer:people[0],shares:[1,2,0],settled:false};expect(balances([bill])).toEqual([80,-80,0]);expect(transfers([bill])).toEqual([{from:people[1],to:people[0],amount:80}]);});
it('已结算账单不参与应收应付',()=>{expect(balances(seed().bills.map(b=>({...b,settled:true})))).toEqual([0,0,0]);});
it('金额和付款人解析明确，未写金额返回失败',()=>{expect(parseBill('许知夏买咖啡花了68元')).toMatchObject({amount:68,payer:people[2]});expect(parseBill('买了纸巾')).toBeNull();expect(parseBill('0元')).toBeNull();});
it('演示数据包含三位室友与有效比例',()=>{const s=seed();expect(s.tasks.length).toBeGreaterThan(0);expect(s.items.filter(i=>i.stock<=i.threshold).length).toBe(3);expect(s.bills.every(b=>b.shares.reduce((a,b)=>a+b,0)>0)).toBe(true);});
});
import {nextTask} from './data';
it('周期完成创建下一次并公平轮换',()=>{const next=nextTask({id:'1',name:'厨房',owner:people[0],date:'2026-10-21',cycle:'每周',done:false});expect(next?.date).toBe('2026-10-28');expect(next?.owner).toBe(people[1]);expect(next?.done).toBe(false);expect(nextTask({id:'1',name:'厨房',owner:people[0],date:'2026-10-21',cycle:'一次性',done:false})).toBeNull()});
import {splitAmounts} from './data';
it('分摊以分为单位，尾差分配后总额保持一致',()=>{const b={...seed().bills[0],amount:100,settled:false};expect(splitAmounts(b)).toEqual([33.34,33.33,33.33]);expect(Math.round(balances([b]).reduce((a,v)=>a+v,0)*100)).toBe(0)});
