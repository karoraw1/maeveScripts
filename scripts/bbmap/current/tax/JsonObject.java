package tax;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map.Entry;

public class JsonObject {

	public static void main(String[] args){
		JsonObject bob=new JsonObject("bob");
		JsonObject joe=new JsonObject("joe");
		JsonObject sue=new JsonObject("sue");
		JsonObject dan=new JsonObject("dan");
		bob.add(joe);
		bob.add(sue);
		joe.add(dan);
		bob.add("a","1");
		bob.add("b","2");
		bob.add("c","3");
		bob.add("a","4");
		dan.add("e","5");
		dan.add("f","6");
		sue.add("g","7");

		System.out.println("dan:\n"+dan);
		System.out.println("sue:\n"+sue);
		System.out.println("joe:\n"+joe);
		System.out.println("bob:\n"+bob);
	}
	
	public JsonObject(String name_){
		name=name_;
	}
	
	public JsonObject(String name_, String key, Object value){
		name=name_;
		add(key, value);
	}

	public void add(String key, Object value){
//		if(smap==null){smap=new LinkedHashMap<String, String>();}
		smap.put(key, value);
	}

	public void add(JsonObject value){
		if(value==null){return;}
//		if(jmap==null){jmap=new LinkedHashMap<String, JsonObject>();}
		int x=2;
		final String name=value.name;
		while(jmap.containsKey(value.name)){
			value.name=name+" "+x;
			x++;
		}
		jmap.put(value.name, value);
	}
	
	public static String toString(ArrayList<JsonObject> list) {
		StringBuilder sb=new StringBuilder();
		sb.append('{');
		int commas=list.size()-1;
		for(JsonObject j : list){
			j.append(0, sb);
			if(commas>0){
				sb.append(",\n");
			}
			commas--;
		}
		sb.append('}');
		return sb.toString();
	}
	
	@Override
	public String toString(){
		
//		if(name==null && jmap.size()==0 && smap.size()<=1){
//			return(smap.size()==0 ? "{}" : "{\"error\": \"Not found.\"}")
//		}
		
		StringBuilder sb=new StringBuilder();
		sb.append('{');
		append(0, sb);
		sb.append('}');
		return sb.toString();
	}
	
	public void append(int level, StringBuilder sb){
		int pad=3*level;
		int pad2=3*(level+1);
		
		if(name!=null){
			for(int i=0; i<pad; i++){sb.append(' ');}
			sb.append('"').append(name).append("\": {\n");
		}
		int commas=smap.size()+jmap.size()-1;
		
		for(Entry<String, Object> e : smap.entrySet()){
			String key=e.getKey();
			Object value=e.getValue();
			for(int i=0; i<pad2; i++){sb.append(' ');}
			if(value!=null && value.getClass()!=String.class){
				sb.append('"').append(key).append("\": ").append(value);
			}else{
				sb.append('"').append(key).append("\": \"").append(value).append('"');
			}
			if(commas>0){sb.append(",\n");}
			else{sb.append('\n');}
			commas--;
		}

		for(Entry<String, JsonObject> e : jmap.entrySet()){
			JsonObject value=e.getValue();
			value.append(level+1, sb);
			if(commas>0){sb.append(",\n");}
			else{sb.append("\n");}
			commas--;
		}
		
		if(name!=null){
			for(int i=0; i<pad; i++){sb.append(' ');}
			sb.append('}');
		}
	}
	
	public String name;
	public final LinkedHashMap<String, Object> smap=new LinkedHashMap<String, Object>();
	public final LinkedHashMap<String, JsonObject> jmap=new LinkedHashMap<String, JsonObject>();
	
}
