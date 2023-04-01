*** Test Cases ***
Test Opaque
	Opaque

Test Inline
	Inline

Test Inline Loop
	Inline Loop

Test Unroll
	Unroll

Test Inline Unroll
	Inline Unroll

Test Nested Inline Unroll
	Nested Inline Unroll

	TRY
		Inline Unroll
	EXCEPT
		Inline Unroll
	END

	TRY
		Fail
		Inline Unroll
	EXCEPT
		Inline Unroll
	END

	IF	${true}
		Inline Unroll
	ELSE
		Inline Unroll
	END

	IF	${false}
		Inline Unroll
	ELSE
		Inline Unroll
	END

*** Keywords ***
Opaque
	[Tags]	opaque
	${x}	${y}	No Operation
	Log		Hello
	RETURN

Inline
	[Tags]	inline
	Opaque
	Opaque

Inline Loop
	[Tags]	inline
	FOR	${i}	IN RANGE	5
		Run Keyword	Log	${i}
	END

Unroll
	[Tags]	unroll
	FOR	${i}	IN RANGE	5
		Opaque
	END

Inline Unroll
	[Tags]	inline	unroll
	FOR	${i}	IN RANGE	5
		Opaque
	END

Nested Inline Unroll
	Inline Unroll
