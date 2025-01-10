"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp
import operator


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.12/Include/internal/pycore_frame.h

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code: types.CodeType = frame_code
        self.builtins: dict[str, tp.Any] = frame_builtins
        self.globals: dict[str, tp.Any] = frame_globals
        self.locals: dict[str, tp.Any] = frame_locals
        self.data_stack: tp.Any = []
        self.return_value: tp.Any = None
        self.instructions = list(dis.get_instructions(self.code))
        self.index = {x.offset: i for i, x in enumerate(self.instructions)}
        self.ind: int = 0
        self.simple_ops: dict[str, tp.Callable[[tp.Any, tp.Any], tp.Any]] = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '%': lambda x, y: x % y,
            '**': lambda x, y: x ** y,
            '/': lambda x, y: x / y,
            '//': lambda x, y: x // y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
            '&': lambda x, y: x & y,
            '|': lambda x, y: x | y,
            '^': lambda x, y: x ^ y,
            '+=': lambda x, y: x + y,
            '-=': lambda x, y: x - y,
            '*=': lambda x, y: x * y,
            '%=': lambda x, y: x % y,
            '**=': lambda x, y: x ** y,
            '/=': lambda x, y: x / y,
            '//=': lambda x, y: x // y,
            '<<=': lambda x, y: x << y,
            '>>=': lambda x, y: x >> y,
            '&=': lambda x, y: x & y,
            '|=': lambda x, y: x | y,
            '^=': lambda x, y: x ^ y,
        }

        self.binary_ops: dict[str, tp.Callable[[tp.Any, tp.Any], tp.Any]] = {
            'POWER': pow,
            'MULTIPLY': operator.mul,
            'DIVIDE': getattr(operator, 'div', lambda x, y: None),
            'FLOOR_DIVIDE': operator.floordiv,
            'TRUE_DIVIDE': operator.truediv,
            'MODULO': operator.mod,
            'ADD': operator.add,
            'SUBTRACT': operator.sub,
            'SUBSCR': operator.getitem,
            'LSHIFT': operator.lshift,
            'RSHIFT': operator.rshift,
            'AND': operator.and_,
            'XOR': operator.xor,
            'OR': operator.or_,
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge,
            'in': lambda x, y: x in y,
            'not in': lambda x, y: x not in y,
            'is': lambda x, y: x is y,
            'is not': lambda x, y: x is not y,
            'exception match': lambda x, y: issubclass(x, Exception) and issubclass(x, y),
        }
        self.unary_ops: dict[str, tp.Callable[[tp.Any], tp.Any]] = {
            'POSITIVE': operator.pos,
            'NEGATIVE': operator.neg,
            'NOT': operator.not_,
            'CONVERT': repr,
            'INVERT': operator.invert,
        }

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        if self.data_stack:
            return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        while self.ind < len(self.instructions):
            f = self.instructions[self.ind].opname.lower() + "_op"
            getattr(self, f)(self.instructions[self.ind].argval)
            self.ind += 1
        return self.return_value

    def load_build_class_op(self, arg: tp.Any) -> None:
        self.push(builtins.__build_class__)

    def resume_op(self, arg: int) -> tp.Any:
        pass

    def precall_op(self, arg: int) -> tp.Any:
        pass

    def push_null_op(self, arg: int) -> tp.Any:
        pass

    def call_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-CALL
        """
        args = self.popn(arg)
        x = self.pop()
        if callable(x):
            self.push(x(*args))
        else:
            self.push(x)

    def load_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-LOAD_NAME
        """
        arg = self.instructions[self.ind].argval
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError(arg)

    def load_locals_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-LOAD_LOCALS
        """
        self.push(self.locals)

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-LOAD_GLOBAL
        """
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise NameError(f"Name {arg} is not defined")

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-LOAD_CONST
        """
        self.push(arg)

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-RETURN_VALUE
        """
        self.return_value = self.pop()
        self.ind = len(list(dis.get_instructions(self.code)))

    def yield_value_op(self, arg: tp.Any) -> tp.Any:
        self.return_value = self.top()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-POP_TOP
        """
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-MAKE_FUNCTION
        """

        code = self.pop()

        if arg & 0x08:
            self.pop()

        if arg & 0x04:
            self.pop()

        if arg & 0x02:
            kw_defaults = self.pop()
        else:
            kw_defaults = {}

        if arg & 0x01:
            defaults = self.pop()
        else:
            defaults = {}

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:

            parsed_args: dict[str, tp.Any] = {}
            pos_only_count = code.co_posonlyargcount
            kw_only_count = code.co_kwonlyargcount
            temp_ind = 0
            args_name = None
            kwargs_name = None
            kw_flag: bool = bool(code.co_flags & 8)
            arg_flag: bool = bool(code.co_flags & 4)
            if arg_flag:
                args_name = code.co_varnames[code.co_argcount + kw_only_count - code.co_nlocals]
            if kw_flag:
                kwargs_name = code.co_varnames[code.co_argcount + kw_only_count + bool(args_name)]

            varnames_list = list(code.co_varnames[:code.co_argcount + kw_only_count])

            for name in varnames_list[:pos_only_count]:
                if name in kwargs and kwargs_name is None:
                    raise TypeError

                if temp_ind == len(args):
                    if name in defaults:
                        parsed_args[name] = defaults[name]
                    else:
                        raise TypeError
                else:
                    parsed_args[name] = args[temp_ind]
                    temp_ind += 1

            for name in varnames_list[pos_only_count:len(varnames_list) - kw_only_count]:
                if name in kwargs:
                    parsed_args[name] = kwargs[name]
                    continue

                if temp_ind == len(args):
                    if name in defaults:
                        parsed_args[name] = defaults[name]
                    else:
                        raise TypeError
                else:
                    parsed_args[name] = args[temp_ind]
                    temp_ind += 1

            if args_name is not None:
                parsed_args[args_name] = tuple(args[temp_ind:])
            elif temp_ind != len(args):
                raise TypeError

            for name in varnames_list[len(varnames_list) - code.co_kwonlyargcount:]:
                if name in kwargs:
                    parsed_args[name] = kwargs[name]
                elif name in kw_defaults:
                    parsed_args[name] = kw_defaults[name]
                else:
                    raise TypeError

            temp_dict = {key: val for key, val in kwargs.items() if
                         key not in parsed_args or key in varnames_list[:pos_only_count]}

            if kwargs_name is not None:
                parsed_args[kwargs_name] = temp_dict
            elif len(temp_dict):
                raise TypeError

            f_locals = dict(self.locals)
            f_locals.update(parsed_args)
            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.12.5/library/dis.html#opcode-STORE_NAME
        """
        const = self.pop()
        self.locals[arg] = const

    def nop_op(self, arg: tp.Any) -> None:
        pass

    def kw_names_op(self, arg: tp.Any) -> None:
        pass

    def store_global_op(self, arg: str) -> None:
        self.globals[arg] = self.pop()

    def store_fast_op(self, arg: str) -> None:
        self.locals[arg] = self.pop()

    def store_attr_op(self, arg: str) -> None:
        setattr(self.pop(), arg, self.pop())

    def binary_slice_op(self, arg: tp.Any) -> None:
        end = self.pop()
        start = self.pop()
        container = self.pop()
        self.push(container[start:end])

    def binary_subscr_op(self, arg: tp.Any) -> None:
        key = self.pop()
        container = self.pop()
        self.push(container[key])

    def store_slice_op(self, arg: tp.Any) -> None:
        end = self.pop()
        start = self.pop()
        container = self.pop()
        values = self.pop()
        container[start:end] = values
        self.push(container)

    def unpack_sequence_op(self, arg: int) -> None:
        seq = self.pop()
        for item in reversed(seq):
            self.push(item)

    def jump_forward_op(self, arg: int) -> None:
        self.ind = self.index[arg] - 1

    def jump_backward_op(self, arg: int) -> None:
        self.ind = self.index[arg] - 1

    def jump_backward_no_interrupt_op(self, arg: int) -> None:
        self.ind = self.index[arg] - 1

    def pop_jump_if_true_op(self, offset: int) -> None:
        if self.pop():
            self.jump_forward_op(offset)

    def pop_jump_if_none_op(self, offset: int) -> None:
        if self.pop() is None:
            self.jump_forward_op(offset)

    def pop_jump_if_false_op(self, offset: int) -> None:
        if not self.pop():
            self.jump_forward_op(offset)

    def jump_if_true_or_pop_op(self, offset: int) -> None:
        if self.top():
            self.jump_forward_op(offset)
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, offset: int) -> None:
        if not self.top():
            self.jump_forward_op(offset)
        else:
            self.pop()

    def extended_arg_op(self, arg: tp.Any) -> None:
        pass

    def get_iter_op(self, arg: tp.Any) -> None:
        self.push(iter(self.pop()))

    def for_iter_op(self, arg: tp.Any) -> None:
        try:
            it = self.pop()
            val = next(it)
            self.push(it)
            self.push(val)
        except StopIteration:
            self.jump_forward_op(arg)
            self.pop()

    def end_for_op(self, arg: tp.Any) -> None:
        if self.data_stack:
            self.pop()
        if self.data_stack:
            self.pop()

    def load_fast_op(self, arg: str) -> None:
        self.push(self.locals[arg])

    def load_fast_and_clear_op(self, arg: str) -> None:
        if arg in self.locals:
            value = self.locals[arg]
        else:
            value = None
        self.locals[arg] = None
        self.push(value)

    def load_fast_check_op(self, arg: str) -> None:
        if arg in self.locals:
            self.push(self.locals[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])
        else:
            raise UnboundLocalError

    def pop_jump_forward_if_none_op(self, arg: int) -> None:
        if self.pop() is None:
            self.jump_forward_op(arg)

    def pop_jump_forward_if_not_none_op(self, arg: int) -> None:
        item = self.pop()
        if item is not None:
            self.jump_forward_op(arg)

    def build_slice_op(self, arg: int) -> None:
        seq = self.popn(arg)
        self.push(slice(*seq))

    def binary_op_op(self, arg: tp.Any) -> None:
        x = self.pop()
        y = self.pop()

        op = self.instructions[self.ind].argrepr
        try:
            result = self.simple_ops[op](y, x)
            self.push(result)
        except RuntimeError:
            raise RuntimeError

    def compare_op_op(self, arg: str) -> None:
        x, y = self.popn(2)
        self.push(self.binary_ops[arg](x, y))

    def build_list_op(self, arg: int) -> None:
        self.push(list(self.popn(arg)))

    def store_subscr_op(self, arg: tp.Any) -> None:
        value, collection, key = self.popn(3)
        collection[key] = value

    def delete_name_op(self, arg: str) -> None:
        del self.locals[arg]

    def delete_subscr_op(self, arg: tp.Any) -> None:
        collection, key = self.popn(2)
        del collection[key]

    def list_extend_op(self, i: int) -> None:
        iterable = self.pop()
        list.extend(self.data_stack[-i], iterable)

    def build_const_key_map_op(self, count: int) -> None:
        keys = self.pop()
        vals = self.popn(count)
        self.push(dict(zip(keys, vals)))

    def build_set_op(self, count: int) -> None:
        values = self.popn(count)
        self.push(set(values))

    def set_update_op(self, i: int) -> None:
        iterable = self.pop()
        set.update(self.data_stack[-i], iterable)

    def format_value_op(self, flags: int) -> None:
        pass

    def build_string_op(self, arg: int) -> None:
        values = map(str, self.popn(arg))
        self.push("".join(values))

    def unary_positive_op(self, arg: tp.Any) -> None:
        self.push(operator.pos(self.pop()))

    def unary_negative_op(self, arg: tp.Any) -> None:
        self.push(operator.neg(self.pop()))

    def unary_not_op(self, arg: tp.Any) -> None:
        self.push(operator.not_(self.pop()))

    def unary_convert_op(self, arg: tp.Any) -> None:
        self.push(repr(self.pop()))

    def unary_invert_op(self, arg: tp.Any) -> None:
        self.push(operator.invert(self.pop()))

    def is_op_op(self, arg: int) -> None:
        left = self.pop()
        right = self.pop()
        if arg:
            self.push(left is not right)
        else:
            self.push(left is right)

    def raise_varargs_op(self, arg: int) -> None:
        if arg == 0:
            raise
        elif arg == 1:
            a = self.pop()
            raise a
        elif arg == 2:
            a = self.pop()
            b = self.pop()
            raise b(a)

    def build_map_op(self, arg: int) -> None:
        data = self.popn(2 * arg)
        item_map = dict()
        for i in range(0, 2 * arg, 2):
            item_map[data[i]] = data[i - 1]
        self.push(item_map)

    def map_add_op(self, arg: int) -> None:
        val = self.pop()
        key = self.pop()
        dict.__setitem__(self.data_stack[-arg], key, val)

    def set_add_op(self, arg: int) -> None:
        value = self.pop()
        set.add(self.data_stack[-arg], value)

    def copy_op(self, arg: int) -> None:
        self.push(self.top())

    def load_method_op(self, arg: str) -> None:
        self.push(getattr(self.pop(), arg))

    def build_tuple_op(self, arg: int) -> None:
        values = self.popn(arg)
        self.push(tuple(values))

    def contains_op_op(self, arg: int) -> None:
        a = self.pop()
        b = self.pop()
        if arg:
            self.push(b not in a)
        else:
            self.push(b in a)

    def import_name_op(self, arg: str) -> None:
        a, b = self.popn(2)
        self.push(__import__(arg, self.globals, self.locals, b, a))

    def import_from_op(self, arg: str) -> None:
        self.push(getattr(self.top(), arg))

    def load_attr_op(self, arg: str) -> None:
        self.push(getattr(self.pop(), arg))

    def delete_attr_op(self, name: str) -> None:
        delattr(self.pop(), name)

    def delete_global_op(self, name: str) -> None:
        del self.globals[name]

    def delete_fast_op(self, name: str) -> None:
        del self.locals[name]

    def return_const_op(self, arg: tp.Any) -> None:
        self.return_value = arg
        self.ind = len(list(dis.get_instructions(self.code)))

    def swap_op(self, i: int) -> None:
        self.data_stack[-1], self.data_stack[-i] = self.data_stack[-i], self.data_stack[-1]

    def call_intrinsic_1_op(self, arg: tp.Any) -> None:
        """
        Calls an intrinsic function with one argument from the stack.
        The argument is taken from the top of the stack, and the result replaces it.
        """
        operand = self.instructions[self.ind].argrepr
        if operand == "INTRINSIC_PRINT":
            print(self.pop())
            self.return_value = arg
        elif operand == "INTRINSIC_IMPORT_STAR":
            module_name = self.pop()
            self.push(__import__(module_name.__name__, self.globals, self.locals))
            for name in dir(module_name):
                if name not in self.locals:
                    self.locals[name] = getattr(module_name, name)
                if name not in self.globals:
                    self.globals[name] = getattr(module_name, name)
        elif operand == "INTRINSIC_LIST_TO_TUPLE":
            lst = self.pop()
            result = tuple(lst)
            self.push(result)
        elif operand == "INTRINSIC_STOPITERATION_ERROR":
            pass
        else:
            raise ValueError(f"dfs{operand} Invalid intrinsic function")

    def call_function_ex_op(self, flags: int) -> None:
        var_set = self.pop() if flags else {}
        args_list = self.pop()
        func = self.pop()
        self.push(func(*args_list, **var_set))

    def setup_annotations_op(self, arg: tp.Any) -> None:
        if '__annotations__' not in self.locals:
            self.locals['__annotations__'] = {}

    def dict_merge_op(self, arg: int) -> None:
        val = self.pop()
        dict1: dict[tp.Any, tp.Any] = self.data_stack[-arg]
        if set(dict1).intersection(val):
            raise KeyError
        dict1.update(val)

    def dict_update_op(self, arg: int) -> None:
        val = self.pop()
        dict1: dict[tp.Any, tp.Any] = self.data_stack[-arg]
        dict1.update(val)

    def list_append_op(self, arg: int) -> None:
        val = self.pop()
        list.append(self.data_stack[-arg], val)


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
