# `rcheck`

Runtime type checking.

---

Functions that return a boolean:
* `is_<type>` such as `is_int`, `is_bool`, etc...
* `is_opt_<type>` such as `is_opt_int`, `is_opt_bool`, etc.. for optional types

Functions that raise exceptions:
* `assert_<type>` such as `assert_int`, `assert_bool`, etc...
* `assert_opt_<type>` such as `assert_opt_int`, `assert_opt_bool`, etc... for optional types
