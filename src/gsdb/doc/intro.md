# yxdb
yxdb提供了针对django ORM和mongoengine的一些扩展和辅助函数。

## 安装
可以直接通过pip安装git上的master最新版本

    pip install -e git+git@git.ikaka.org:libs/yxdb.git#egg=yxdb

## 辅助函数/装饰器

### .get 函数
针对django的Model，和mongoengine类型增加，是.objects.get的一层封装，对_DoesNotExxist_和_ValidationError_会直接返回_None_，在返回结果多于一个时会抛出_MultipleObjectsReturned_。使用举例

    user = User.get(username="abc@abc.com")
	tag = SystemTag.get(name="代数", soft_del=False)
	timu = Timu.get(id="43e2b857123409abcdef")

.get函数在工程中第一次import过yxdb后，就会和django/mongoengine绑定。

### random_select 函数
用于从一个mongoengine Document中随机选取一个document返回，使用的条件是Document本身需要有一个取值范围在0~1(可以由_random.random()_生成)float类型的字段（需要对此字段建索引），默认的字段名称为_rnd_。

使用方法为

    random_select(document, rnd_column='rnd', filters=None)
    参数:
	document: Document类，如User, Question等
	rnd_column: string, default 'rnd', 存储随机数权重的字段名称。
	filters: dict, optional, 查询条件。

范例:

    from yxdb import random_select
	# 随机获取没有被删除的一道科目为"chuzhongshuxue"的题目
    t = random_select(Timu, filters={'soft_del': False, 'kemu':'chuzhongshuxue'})

在找不到符合条件的结果时，会返回None。可以手动给Document的_rnd_字段赋值，来修改随机产生的分布。

### ._iter 函数
.iter函数用于通过cursor方式对某一个document的全部元素进行分页的遍历，仅支持上一页，下一页。.iter在import了yxdb之后和Document类进行绑定，之后即可通过Document.iter()进行调用。

使用方法:

    document_iter(document, threshold=None, index_column='id',
                  desc=False, filters=None, limit=None)
	参数:
	document: Document类
	threshold: 一个可以用于比较的value，对应于index_column字段的值。
	index_column: string, 用于排序的字段名称，默认为'id'.
	desc: boolean, default False, 是否降序排列.
	filters: dict, optional, 查询条件.
	limit: int, optional, 返回结果的数量限制.
	返回:
	一个tuple类型结果(ret, last_id), 其中
	ret为Document类的对象的列表，是查询的当前页的结果;
	last是最后一个对象index_column的值，用于获取下一页时，作为threshold传入.
	

范例：

    # 遍历题目，每页10个
	# 获取第一页
	ret, last_id = Timu._iter(filters={'kemu':'gaozhongwuli', 'soft_del': False},
	                          limit=10)
	# 获取第二页
	ret, last_id = Timu._iter(threshold=last_id,
	                          filters={'kemu':'gaozhongwuli', 'soft_del': False},
                              limit=10)

一般来说，分页多采用.count()获取总页数，并且用page_num获取offset，但对于mongodb和mysql来说，这样的分页方式需要大量的扫描collection或者数据表项目，是性能的主要杀手之一。使用iter可以避免大量的表扫描，不过没有直接跳至某一页的能力。

### Decorator change_lut_on_save
是Document的class的decorator，用于在.save()被调用时，同时修改对象的.lut字段为当前的时间(datetime.datetime.now())。

范例

    import yxdb
    @yxdb.change_lut_on_save
	class SomeDocument(Document):
	    lut = DateTimeField()


### switch_read_preference 切换ReadPreference上下文
switch\_read\_preference 用于在一个with语句的范围内切换ReadPreference的上下文。比如，如果连接的默认ReadPreference是SECONDARY_PREFERRED, 但是我们希望在某些代码内直接从PRIMARY读取，那么可以按照如下的方法来使用_switch\_read\_preference_ (注意_switch\_rp_与_switch\_read\_preference_一样):

    import yxdb
    with yxdb.switch_rp('PRIMARY'):
	    # your code

使用方法:

    with switch_rp(preference, tag_sets_disabled=False)
	参数
	preference: 为ReadPreference累的属性，包括:
            ReadPreference.NEAREST
            ReadPreference.PRIMARY
            ReadPreference.PRIMARY_PREFERRED
            ReadPreference.SECONDARY
            ReadPreference.SECONDARY_ONLY
            ReadPreference.SECONDARY_PREFERRED
       或者是对应属性的字符串名:
            'NEAREST', 'PRIMARY', 'PRIMARY_PREFERRED', 'SECONDARY',
            'SECONDARY_ONLY', 'SECONDARY_PREFERRED'
	tag_sets_disabled: boolean, default False, 因为当preference为
	     ReadPreference.PRIMARY时，会和connection的tag_sets的设置
		 冲突，所以如果没有设置tag_sets, 需要设置此属性为True. 在
		 tag_sets_disabled==False的情况下，如果switch context到PRIMARY,
		 那么会自动被重新设置成PRIMARY_PREFERRED.

使用场景:

- 在使用分布式锁的场景下，要手动切换ReadPreference到PRIMARY，以保证被锁住的数据的一致性

    with cache_lock("the_lock_name"):
	    with yxdb.switch_rp("PRIMARY"):
		    # your code
