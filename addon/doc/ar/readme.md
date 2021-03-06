# أقسام المفضلة #
# الإصدار 21.01-dev #

* المطورون : عبد الرحيم, وعبد الله زين الدين, وعبد الكريم.
* تحميل [الإصدار الجاهز](https://github.com/abdel792/myFavoriteTopics/releases/download/v3.0/myFavoriteTopics-3.0.nvda-addon)
* تحميل [الإصدار التجريبي](https://github.com/abdel792/myFavoriteTopics/releases/download/v3.0-dev/myFavoriteTopics-3.0-dev.nvda-addon)

تتيح لك هذه الإضافة عرض وتصَفُح الأقسام المفضلة لديك.

ستجد عنصرا ضمن قائمة "أدوات" nvda تحت عنوان "أقسام المفضلة", الذي يمكنك من فتح مربع حوار يتألف من 5 أزرار :

* زر "عرض المواقع المفضلة", لعرض قائمة المواقع المفضلة لديك.
* زر "عرض البرامج المفضلة", لعرض قائمة البرامج والمجلدات المفضلة لَديكَ والموجودة على حاسوبك.
* زر "عرض الاتصالات المفضلة", لعرض قائمة الاتصالات المفضلة لديك.
* زر "عرض الجرائد المفضلة", لعرض قائمة الجرائد المفضلة لديك.
* زر "إغلاق", لإعادة إغلاق مربع الحوار.

## ملاحظات ##

* بالإمكان إعادة إغلاق مربع الحوار هذا بمجرد الضغط على زر الهروب.
* بإمكانك تعيين اختصار لفتح مربع الحوار هذا انطلاقا من قائمة "تخصيص الاختصارات" وبالتحديد, في صِنْف "أدوات".

## للتنقل بين عناصر القائمة ##

عند الضغط على الزر المطابِق لقسم ما, سيظهر مربع حوار مكوَن من العناصر التالية :

* قائمة من العناصر, يمكن التحرك بينها باستخدام تاب وشيفت وتاب;
* زر "فتح", الذي يسمح لك بالدخول إلى محتوى العنصر المحدد في القائمة.
* زر "إضافة مجموعة جديدة", الذي يسمح لك بإضافة مجموعة جديدة إلى القائمة 
* زر "إضافة مفتاح جديد", الذي يسمح لك بإضافة مفتاح جديد إلى القائمة.
* زر "إعادة تسمية المجموعة", الذي يسمح لك بإعادة تسمية المجموعة المحددة في القائمة. (لا يبرز هذا العنصر إلا إذا كان العنصر المحدد عبارة عن مجموعة)
* زر "إعادة تسمية المفتاح", الذي يسمح لك بإعادة تسمية المفتاح المحدد في القائمة. (لا يبرز هذا العنصر إلا إذا كان العنصر المحدد عبارة عن مفتاح)
* زر "تعديل المحتوى", الذي يسمح لك بتعديل محتوى المفتاح المطابق للعنصر المحدد في القائمة. (لا يبرز هذا العنصر إلا إذا كان العنصر المحدد عبارة عن مفتاح)
* زر "نقل إلى مجموعة", الذي يسمح لك بنقل المفتاح المحدد في القائمة إلى مجموعة. (لا يبرز هذا العنصر إلا إذا كان العنصر المحدد عبارة عن مفتاح)
* زر "حَذف", الذي يسمح لك بحَذف العنصر المحدد في القائمة. إذا كان العنصر عبارة عن مجموعة فإنَّ جميع محتويات هذه المجموعة سيتم حَذْفُهَا.
* زر "إغلاق", لإعادة إغلاق مربع الحوار.

## ملاحظات ##

* يمكن الضغط على زر الهروب لإعادة إغلاق أَي من مربعات الحوار هذه والرجوع إلى مربع الحوار الرئيسي الذي يضم إزرار الدخول إلى أقسام المفضلة;
* عند التنقل بين عناصر القائمة, وتكون بصدد المرور على مجموعة سيكون اسمها مقترنا بمصطلح (مجموعة);
* حين تفْتحُ مجموعة, ستكون بإزائ قائمة المفاتيح التي تحتويها هذه المجموعة;
* بإمكانك تعيين اختصار خاص لفتح كل مربع حوار على حِدَة من مربعات الحوار المذكورة في الأقسام السابقة, انطلاقا من قائمة "تخصيص الاختصارات" وتحديدا, في صِنْف "أدوات";
* عند عدم وجود أي عنصر بالقائمة, سيتم الاقتصار على عرض الأزرار "إضافة مجموعة جديدة", و"إضافة مفتاح جديد", و"إغلاق".

## مستجدات الإصدار 3.0 ##

* إضافة التوافق مع إصدارات NVDA التي تستعمل Python 3.

## مستجدات الإصدار 2.0 ##

* إصلاح الخلل الذي كان يحدث بعد إغلاق مربع حوار أقسام المفضلة والذي كان يمنع إعادة فتْحِها دون إعادة تشغيل nvda.

## مستجدات الإصدار 1.2 ##

* هذا الإصدار يحقق توافقية الإضافة مع wxPython الإصدار 4, وخاصة بالنسبة لمربعات الحوار عند تعديل محتويات المفاتيح وإعادة تسمية المفاتيح والمجموعات الخاصة بكل قسم;

## مستجدات الإصدار 1.1. ##

* هذا الإصدار يضيف إمكانية إنشاء وإدارة مجموعات بالأقسام الفرعية;
* في قسم "عرض الاتصالات المفضلة", يتم عرض معلومات جهات الاتصال داخل نص متعدد الأسطر, تسهيلًا لعملية النسخ;
* من الآن فصاعدا, في قسم "الاتصالات المفضلة", محتويات كل جهة اتصال تُدْرَج ضمنَ نص متعدد الأسطر.

## مستجدات الإصدار 1.0. ##

* الإصدار الأول.

