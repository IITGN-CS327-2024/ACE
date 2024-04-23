(module
	(func $add (export "add") 		(param $a1 i32) 		(param $b1 i32) (result i32)
		(local.get $a1)
		(local.get $b1)
		(i32.add)

	)
	(func $sub (export "sub") 		(param $a1 i32) 		(param $b1 i32) (result i32)
		(local.get $a1)
		(local.get $b1)
		(i32.sub)

	)
	(func $mul (export "mul") 		(param $a1 i32) 		(param $b1 i32) (result i32)
		(local.get $a1)
		(local.get $b1)
		(i32.mul)

	)
	(func $div (export "div") 		(param $a1 i32) 		(param $b1 i32) (result i32)
		(local.get $a1)
		(local.get $b1)
		(i32.div)

	)
	(func $mod (export "mod") 		(param $a1 i32) 		(param $b1 i32) (result i32)
		(local.get $a1)
		(local.get $b1)
		(i32.mod)

	)
	(func $main (result i32)
	)
	)
