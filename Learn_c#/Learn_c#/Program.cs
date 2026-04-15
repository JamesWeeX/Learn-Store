using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Learn_c_
{
    interface IShape
    {
        double Area();
    }
    abstract class Shape: IShape
    {
        public Shape(string name, double length)
        {
            Name = name;
            Length = length;
        }
        public string Name { get; private set; }
        public double Length { get; private set; }
        
        public abstract double Area();
    }

    class Rectangle : Shape
    {
        public Rectangle(string name, double length, double width) : base(name, (length + width) * 2)
        {
            Len = length;
            Width = width;
        }
        public double Len { get; private set; }
        public double Width { get; private set; }
        public override  double Area ()
        {
              return Len * Width;  
        }
    }

    class Triangle : Shape
    {
        public Triangle(string name, double a, double b, double c) : base(name, a + b + c)
        {
            A = a;
            B = b;
            C = c;
        }
        public double A { get; private set; }
        public double B { get; private set; }
        public double C { get; private set; }
        public override  double Area()
        {
             double s = Length / 2;
             return Math.Sqrt(s* (s - A) * (s - B) * (s - C));  
        }
    }


    namespace Tool
    {
        struct Method
        {
            void Add(in int a, out int b) {  b = a+3; }

        }
    }


    internal class Program
    {
        static void PrintInt(IEnumerable lsit)
        {
            foreach (var item in lsit)
            {
                Console.WriteLine(item);
            }

            Console.WriteLine("______________________________");
        }
        static void Main(string[] args)
        {
            Rectangle rt = new Rectangle("rect", 5, 10);
            Triangle tr = new Triangle("tri", 3, 4, 5);

            Console.WriteLine($"Rectangle Area: {rt.Area()}");
            Console.WriteLine($"Triangle Area: {tr.Area()}");

            int[] arr = { 5,8,9,3,0};
            PrintInt(arr);

            ArrayList al = new ArrayList();
            al.Add(5);
            al.Add(2);
            al.Add(-4);
            PrintInt(al);

            List<int> list = new List<int>{ -1,4,-2,-8,7};
            PrintInt(list);
        }
    }
}
