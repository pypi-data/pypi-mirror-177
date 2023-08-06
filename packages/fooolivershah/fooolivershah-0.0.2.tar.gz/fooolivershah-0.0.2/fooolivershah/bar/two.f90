module test2
  
  use test3

  implicit none
    
  contains
  
  subroutine add2(a)

    integer, intent(in) :: a
    integer :: b
    b = a + 2
    print *, 'two',b
    
    call add3(b)

  end subroutine add2

end module test2