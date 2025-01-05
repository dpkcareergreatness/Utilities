/*
 * Creates a compile time assertion if condition specified by 'pred' is not true
 * This macro is used to generate a compile-time error if a certain condition (pred) is not met. 
 * It does this by defining a typedef for a char array with a size that depends on the condition. 
 * If the condition is true, the array size is 1; if false, the array size is -1, which is invalid and will cause a compile-time error.

 * Why typedef and why not declare char MSG##descr?
  * No memory is taken with typedef(it only defines a type not any varialbe in memory)
  * And due to that no clashes with any other variable names

 * example: 
  * #define MACRO(pred, descr) typedef char MSG##descr[(pred)?1:-1]
  * MACRO(sizeof(int) == 4, IntSizeMustBe4);
  * If sizeof(int) != 4, the typedef creates an array of size -1, causing a compile-time error with a message that includes MSGIntSizeMustBe4.
*/

#define MACRO(pred, descr) typedef char MSG##descr[(pred) ? 1 : -1]