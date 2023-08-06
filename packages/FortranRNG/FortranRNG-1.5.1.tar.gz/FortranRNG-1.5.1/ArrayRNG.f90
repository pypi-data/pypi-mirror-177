!subroutine array_percent_true(percent, length, output)
!    implicit none
!    double precision, intent(in) :: percent
!    integer, intent(in) :: length
!    logical, dimension(length), intent(out) :: output
!    call percent_true(percent, output)
!end subroutine array_percent_true
!
!subroutine array_random_below(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call random_below(limit, output)
!end subroutine array_random_below
!
!subroutine array_random_integer(low, high, length, output)
!    implicit none
!    integer, intent(in) :: low, high, length
!    integer, dimension(length), intent(out) :: output
!    call random_integer(low, high, output)
!end subroutine array_random_integer
!
!subroutine array_random_range(start, stop, step, length, output)
!    implicit none
!    integer, intent(in) :: start, stop, step, length
!    integer, dimension(length), intent(out) :: output
!    call random_range(start, stop, step, output)
!end subroutine array_random_range
!
!subroutine array_d(sides, length, output)
!    implicit none
!    integer, intent(in) :: sides, length
!    integer, dimension(length), intent(out) :: output
!    call d(sides, output)
!end subroutine array_d
!
!subroutine array_dice(rolls, sides, length, output)
!    implicit none
!    integer, intent(in) :: rolls, sides, length
!    integer, dimension(length), intent(out) :: output
!    call dice(rolls, sides, output)
!end subroutine array_dice
!
!subroutine array_plus_or_minus(amount, length, output)
!    implicit none
!    integer, intent(in) :: amount, length
!    integer, dimension(length), intent(out) :: output
!    call plus_or_minus(amount, output)
!end subroutine array_plus_or_minus
!
!subroutine array_plus_or_minus_linear(amount, length, output)
!    implicit none
!    integer, intent(in) :: amount, length
!    integer, dimension(length), intent(out) :: output
!    call plus_or_minus_linear(amount, output)
!end subroutine array_plus_or_minus_linear

subroutine array_canonical(length, output)
    implicit none
    integer, intent(in) :: length
    double precision, dimension(length), intent(out) :: output
    call random_number(output)
end subroutine array_canonical

!subroutine array_random_float(low, high, length, output)
!    implicit none
!    double precision, intent(in) :: low, high
!    integer, intent(in) :: length
!    double precision, dimension(length), intent(out) :: output
!    call random_float(low, high, output)
!end subroutine array_random_float
!
!subroutine array_triangular(low, high, mode, length, output)
!    implicit none
!    double precision, intent(in) :: low, high, mode
!    integer, intent(in) :: length
!    double precision, dimension(length), intent(out) :: output
!    call triangular(low, high, mode, output)
!end subroutine array_triangular
!
!subroutine array_random_index(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call random_index(limit, output)
!end subroutine array_random_index
!
!subroutine array_front_linear(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call front_linear(limit, output)
!end subroutine array_front_linear
!
!subroutine array_back_linear(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call back_linear(limit, output)
!end subroutine array_back_linear
!
!subroutine array_middle_linear(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call middle_linear(limit, output)
!end subroutine array_middle_linear
!
!subroutine array_quantum_linear(limit, length, output)
!    implicit none
!    integer, intent(in) :: limit, length
!    integer, dimension(length), intent(out) :: output
!    call quantum_linear(limit, output)
!end subroutine array_quantum_linear
