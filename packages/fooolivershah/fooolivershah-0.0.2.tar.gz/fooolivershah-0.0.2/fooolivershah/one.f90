module test1

    implicit none
  
    contains
  
    subroutine add1(a)
  
      implicit none
      integer :: a
      integer :: b
      b = a + 1
      print *, 'one',b
  
    end subroutine add1
  
  
  end module test1