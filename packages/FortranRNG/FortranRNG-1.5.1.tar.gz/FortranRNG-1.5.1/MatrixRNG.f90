!subroutine matrix_percent_true(percent, length, width, output)
!    implicit none
!    double precision, intent(in) :: percent
!    integer, intent(in) :: length, width
!    logical, dimension(length, width), intent(out) :: output
!    call percent_true(percent, output)
!end subroutine matrix_percent_true
!
!subroutine matrix_random_below(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call random_below(limit, output)
!end subroutine matrix_random_below
!
!subroutine matrix_random_integer(low, high, length, width, output)
!    implicit none
!    integer, intent(in) :: low, high, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call random_integer(low, high, output)
!end subroutine matrix_random_integer
!
!subroutine matrix_random_range(start, stop, step, length, width, output)
!    implicit none
!    integer, intent(in) :: start, stop, step, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call random_range(start, stop, step, output)
!end subroutine matrix_random_range
!
!subroutine matrix_d(sides, length, width, output)
!    implicit none
!    integer, intent(in) :: sides, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call d(sides, output)
!end subroutine matrix_d
!
!subroutine matrix_dice(rolls, sides, length, width, output)
!    implicit none
!    integer, intent(in) :: rolls, sides, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call dice(rolls, sides, output)
!end subroutine matrix_dice
!
!subroutine matrix_plus_or_minus(amount, length, width, output)
!    implicit none
!    integer, intent(in) :: amount, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call plus_or_minus(amount, output)
!end subroutine matrix_plus_or_minus
!
!subroutine matrix_plus_or_minus_linear(amount, length, width, output)
!    implicit none
!    integer, intent(in) :: amount, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call plus_or_minus_linear(amount, output)
!end subroutine matrix_plus_or_minus_linear

subroutine matrix_canonical(length, width, output)
    implicit none
    integer, intent(in) :: length, width
    double precision, dimension(length, width), intent(out) :: output
    call random_number(output)
end subroutine matrix_canonical

!subroutine matrix_random_float(low, high, length, width, output)
!    implicit none
!    double precision, intent(in) :: low, high
!    integer, intent(in) :: length, width
!    double precision, dimension(length, width), intent(out) :: output
!    call random_float(low, high, output)
!end subroutine matrix_random_float
!
!subroutine matrix_triangular(low, high, mode, length, width, output)
!    implicit none
!    double precision, intent(in) :: low, high, mode
!    integer, intent(in) :: length, width
!    double precision, dimension(length, width), intent(out) :: output
!    call triangular(low, high, mode, output)
!end subroutine matrix_triangular
!
!subroutine matrix_random_index(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call random_index(limit, output)
!end subroutine matrix_random_index
!
!subroutine matrix_front_linear(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call front_linear(limit, output)
!end subroutine matrix_front_linear
!
!subroutine matrix_back_linear(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call back_linear(limit, output)
!end subroutine matrix_back_linear
!
!subroutine matrix_middle_linear(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call middle_linear(limit, output)
!end subroutine matrix_middle_linear
!
!subroutine matrix_quantum_linear(limit, length, width, output)
!    implicit none
!    integer, intent(in) :: limit, length, width
!    integer, dimension(length, width), intent(out) :: output
!    call quantum_linear(limit, output)
!end subroutine matrix_quantum_linear
