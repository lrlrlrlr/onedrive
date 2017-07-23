from multiprocessing import pool



from multiprocessing import Pool
import os,time,random

result=[]#存储结果的列表


def long_time_task(name):#等待随机时间,return随机时间
	print('Run task %s(%s)...'%(name,os.getpid()))
	start=time.time()
	time.sleep(random.random()*3)
	end=time.time()
	print('Task %s run %0.2f sec.'%(name,end-start))

	return end-start


if __name__ == '__main__':
	print('parent:',os.getpid())
	p=Pool(8)

	for i in range(10):
		p.apply_async(long_time_task,args=(i,))#多进程运行函数
	print('waiting for all process done...')
	p.close()
	p.join()

	print('all done!')