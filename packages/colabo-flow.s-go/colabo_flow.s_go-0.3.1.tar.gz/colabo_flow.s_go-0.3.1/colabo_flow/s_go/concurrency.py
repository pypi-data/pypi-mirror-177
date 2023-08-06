import threading
import asyncio
from typing import Any
from yachalk import chalk

def asyncio__provide_loop(appNameTextWithContext):
	global asyncio_loop
	# asyncio_loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(asyncio_loop)

	try:
		current_running_loop = asyncio.get_running_loop()
		print(f"{appNameTextWithContext('_start_consuming')} current_running_loop: {current_running_loop}")
		asyncio_loop = current_running_loop
	except Exception as err:
		print(f"{appNameTextWithContext('_start_consuming')} Error (asyncio.get_running_loop()): {err}")

	if(not asyncio_loop):
		try:
			# should trigger creating a asyncio loop
			event_loop = asyncio.get_event_loop()
			print(f"{appNameTextWithContext('_start_consuming')} event_loop: {event_loop}")
			asyncio_loop = event_loop
		except Exception as err:
			print(f"{appNameTextWithContext('_start_consuming')} Error (asyncio.get_event_loop()): {err}")

	if(not asyncio_loop):
		print(f"{appNameTextWithContext('_start_consuming')} Creating a new loop (asyncio.new_event_loop())")
		asyncio_loop = asyncio.new_event_loop()

	# TODO: should we put it only next to `asyncio_loop = asyncio.new_event_loop()`
	asyncio.set_event_loop(asyncio_loop)

# set of a background tasks that keeps strong references to tasks
# to protect getting them destroyed before they get execution finished
background_tasks = set()

def run_background_task(loop, _lambda):
	"""
	`run_background_task(the_loop, lambda: processColaboFlowMsg_TaskExecute(host, msg))`
	"""

	task = loop.create_task(_lambda())

	# # Add task to the set. This creates a strong reference.
	background_tasks.add(task)

	# To prevent keeping references to finished tasks forever,
	# make each task remove its own reference from the set after
	# completion:
	task.add_done_callback(background_tasks.discard)

async def async_connection_callback_threadsafe(connection, appNameTextWithContext, _lambda)->bool:
	"""
	Executes _lambda function in the context of the connection-thread and
	it provides an await mechanism for waiting for its completion
	"""

	# Get the current event loop.
	loop = asyncio.get_running_loop()

	# Create a new Future object
	futLambdaExecuted = loop.create_future()

	def _runLambdaInContext():
		print(f"{appNameTextWithContext('async_connection_callback_threadsafe:_runLambdaInContext')} start, futLambdaExecuted: {futLambdaExecuted}")
		_lambda()
		# futLambdaExecuted.set_result(True)
		loop.call_soon_threadsafe(futLambdaExecuted.set_result, True)
		print(f"{appNameTextWithContext('async_connection_callback_threadsafe:_runLambdaInContext')} end, futLambdaExecuted: {futLambdaExecuted}")

	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')} before add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")
	connection.add_callback_threadsafe(lambda: _runLambdaInContext())
	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')} awaiting futLambdaExecuted: {futLambdaExecuted}")
	await futLambdaExecuted
	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')} after add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

async def async_run_func_under_thread(appNameTextWithContext, _async_lambda, name)->Any:
	"""
	Executes _async_lambda function in the context of a new thread and
	it provides an await mechanism for waiting for its completion
	"""

	# Get the current event loop.
	external_loop = asyncio.get_running_loop()

	# Create a new Future object
	futLambdaExecuted = external_loop.create_future()

	def threaded_runLambdaUnderThread():
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} start, futLambdaExecuted: {futLambdaExecuted}")

		threaded_asyncio_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(threaded_asyncio_loop)
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} created the asyncio loop: {threaded_asyncio_loop}")

		asyncio.run(_async_lambda())
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} starting: threaded_asyncio_loop.run_forever()")
		threaded_asyncio_loop.run_forever()

		# should not be used, it will not be captured in the calling thread ...
		# futLambdaExecuted.set_result(True)
		# ... but rather call it in the context of the loop of the external thread
		external_loop.call_soon_threadsafe(futLambdaExecuted.set_result, True)
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} end, futLambdaExecuted: {futLambdaExecuted}")

	print(f"{appNameTextWithContext('async_run_func_under_thread')} before add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

	taskThread = threading.Thread(target=threaded_runLambdaUnderThread, args=())
	taskThread.name = f'{name}_{taskThread.name}'
	taskThread.start()
	native_id = taskThread.native_id
	print(f"{appNameTextWithContext('async_run_func_under_thread')} OK, the '{name}' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

	print(f"{appNameTextWithContext('async_run_func_under_thread')} awaiting futLambdaExecuted: {futLambdaExecuted}")
	await futLambdaExecuted
	print(f"{appNameTextWithContext('async_run_func_under_thread')} after add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

def run_func_under_thread(appNameTextWithContext, _async_lambda, name)->Any:
	"""
	Executes _async_lambda function in the context of a new thread and
	it provides an await mechanism for waiting for its completion
	"""

	def threaded_runLambdaUnderThread():
		print(f"{appNameTextWithContext('run_func_under_thread:threaded_runLambdaUnderThread')} started")

		threaded_asyncio_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(threaded_asyncio_loop)
		print(f"{appNameTextWithContext('run_func_under_thread:threaded_runLambdaUnderThread')} created the asyncio loop: {threaded_asyncio_loop}")

		print(f"{appNameTextWithContext('run_func_under_thread:threaded_runLambdaUnderThread')} launching _async_lambda")
		asyncio.run(_async_lambda())
		print(f"{appNameTextWithContext('run_func_under_thread:threaded_runLambdaUnderThread')} starting: threaded_asyncio_loop.run_forever()")
		threaded_asyncio_loop.run_forever()

		print(f"{appNameTextWithContext('run_func_under_thread:threaded_runLambdaUnderThread')} task ended")

	print(f"{appNameTextWithContext('run_func_under_thread')} before add_callback_threadsafe")

	taskThread = threading.Thread(target=threaded_runLambdaUnderThread, args=())
	taskThread.name = f'{name}_{taskThread.name}'
	taskThread.start()
	native_id = taskThread.native_id
	print(f"{appNameTextWithContext('run_func_under_thread')} OK, the '{name}' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

	# print(f"{appNameTextWithContext('run_func_under_thread')} waiting for the thread to finish ...")
	# taskThread.join()
	# print(f"{appNameTextWithContext('run_func_under_thread')} thread finished")
